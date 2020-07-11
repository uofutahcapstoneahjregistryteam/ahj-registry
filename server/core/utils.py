from core.models import *
from simple_history.models import HistoricalRecords
from django.utils import timezone
from rest_framework.response import Response
from core.serializers import *
from rest_framework.parsers import JSONParser
from django.apps import apps
import json
import csv


def get_ahj_diff(ahj):
    new_record = ahj.history.first()
    old_record = ahj.history.first()
    if new_record is None:
        new_record = old_record
    delta = new_record.diff_against(old_record)
    for change in delta.changes:
        print("{} changed from {} to {}".format(change.field, change.old, change.new))


def export_ahjs_csv():
    with open('ahjs_all.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['AHJID', 'AHJName', 'StateProvince'])
        ahjs = AHJ.objects.all()
        count = 1
        for ahj in ahjs:
            writer.writerow([ahj.AHJID, ahj.AHJName, Address.objects.get(AHJ=ahj).StateProvince])
            print('Written AHJ %i' % count)
            count += 1


def export_ahjs_no_polygon_csv():
    with open('ahjs_no_polygon.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['AHJID', 'AHJName', 'StateProvince'])
        ahjs = AHJ.objects.filter(county_mpoly=None).filter(city_mpoly=None)
        count = 1
        for ahj in ahjs:
            writer.writerow([ahj.AHJID, ahj.AHJName, Address.objects.get(AHJ=ahj).StateProvince])
            print('Written AHJ %i' % count)
            count += 1


def export_ahjs_both_polygons_csv():
    with open('ahjs_no_polygon.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['AHJID', 'AHJName', 'StateProvince'])
        ahjs = AHJ.objects.exclude(county_mpoly=None).exclude(city_mpoly=None)
        count = 1
        for ahj in ahjs:
            writer.writerow([ahj.AHJID, ahj.AHJName, Address.objects.get(AHJ=ahj).StateProvince])
            print('Written AHJ %i' % count)
            count += 1


def export_polygons_csv():
    with open('polygons_all.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['NAMELSAD', 'STATEABBR', 'STATEFP'])
        counties = County.objects.all()
        cities = City.objects.all()
        count = 1
        for c in counties:
            writer.writerow([c.NAMELSAD, c.STATEABBR, c.STATEFP])
            print('Written County %i' % count)
            count += 1
        for c in cities:
            writer.writerow([c.NAMELSAD, c.STATEABBR, c.STATEFP])
            print('Written City %i' % count)
            count += 1


def export_polygons_no_ahj_csv():
    with open('polygons_no_ahj.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['NAMELSAD', 'STATEABBR', 'STATEFP'])
        counties = County.objects.filter(ahj=None)
        cities = City.objects.filter(ahj=None)
        count = 1
        for c in counties:
            writer.writerow([c.NAMELSAD, c.STATEABBR, c.STATEFP])
            print('Written County %i' % count)
            count += 1
        for c in cities:
            writer.writerow([c.NAMELSAD, c.STATEABBR, c.STATEFP])
            print('Written City %i' % count)
            count += 1


def export_county_polygon_geoid_csv():
    with open('county_polygon_geoid.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['NAMELSAD', 'STATEABBR', 'GEOID'])
        counties = County.objects.all()
        count = 1
        for c in counties:
            writer.writerow([c.NAMELSAD, c.STATEABBR, c.GEOID])
            print('Written County %i' % count)
            count += 1


def export_city_polygon_geoid_csv():
    with open('city_polygon_geoid.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['NAMELSAD', 'STATEABBR', 'GEOID'])
        cities = City.objects.all()
        count = 1
        for c in cities:
            writer.writerow([c.NAMELSAD, c.STATEABBR, c.GEOID])
            print('Written City %i' % count)
            count += 1


def export_dupe_ahjs_csv():
    with open('dupe_ahjs.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['AHJName', 'STATEABBR'])
        addrs = Address.objects.all().order_by('StateProvince')
        current_state = addrs.first().StateProvince
        temp_addrs = addrs.filter(StateProvince=current_state).order_by('AHJ__AHJName')
        i = 0
        dupe_count = 0
        prev = temp_addrs.first().AHJ.AHJName
        curr = ''
        print('starting loop')
        for x in range(len(addrs)):
            temp_state = addrs[x].StateProvince
            if current_state != temp_state:
                current_state = temp_state
                temp_addrs = addrs.filter(StateProvince=current_state).order_by('AHJ__AHJName')
                print('Filtering State')
                i = 0
            curr = temp_addrs[i].AHJ.AHJName
            if i != 0 and curr == prev:
                dupe_count += 1
                writer.writerow([temp_addrs[i].AHJ.AHJName, temp_addrs[i].StateProvince])
                print('DUPE: %s, %s' % (temp_addrs[i].AHJ.AHJName, temp_addrs[i].StateProvince))
            prev = curr
            print(i)
            i += 1


def create_edit(request):
    edit_serializer = EditSerializer(data=request.data)
    if edit_serializer.is_valid():
        edit = Edit(**edit_serializer.validated_data)
        if edit.EditType == 'create':
            record_serializer = get_record_serializer(json.loads(edit.Value), edit.RecordType)
            if not record_serializer.is_valid():
                return Response(record_serializer.errors)
        elif edit.EditType == 'update':
            record = None
            if edit.RecordType == 'AHJ':
                record = apps.get_model('core', edit.RecordType).objects.filter(AHJID=edit.RecordID).first()
            else:
                record = apps.get_model('core', edit.RecordType).objects.filter(id=edit.RecordID).first()
            if not hasattr(record, edit.FieldName):
                return Response({'detail': 'FieldName not found.'})
            edit.PreviousValue = getattr(record, edit.FieldName)
        edit.ModifyingUserID = request.user.id
        edit.ModifiedDate = timezone.now()
        if request.user.is_superuser or request.user.id == edit.get_record_owner_id():
            edit.IsConfirmed = True
            edit.ConfirmingUserID = request.user.id
            edit.ConfirmedDate = timezone.now()
            edit.VoteRating = 0
            apply_edit(edit)
            return Response(EditSerializer(edit).data)
        else:
            edit.IsConfirmed = False
            edit.ConfirmingUserID = None
            edit.ConfirmedDate = None
            edit.VoteRating = 0
            edit.save()

        return Response({'detail': 'success'})
    return Response(edit_serializer.errors)


def update_edit(request):
    edit = Edit.objects.filter(pk=request.data.get('id')).first()
    if edit is None:
        return Response({'detail': 'Edit not found'})
    edit_serializer = EditSerializer(data=request.data)
    if edit_serializer.is_valid():
        validated_data = edit_serializer.validated_data
        if request.user.is_superuser or request.user.id == edit.get_record_owner_id():
            if not edit.IsConfirmed and validated_data.get('IsConfirmed'):
                edit.IsConfirmed = True
                edit.ConfirmingUserID = request.user.id
                edit.ConfirmedDate = timezone.now()
                apply_edit(edit)
        elif request.user.id == edit.ModifyingUserID:
            if edit.EditType == 'create':
                try:
                    record_serializer = get_record_serializer(json.loads(validated_data.get('Value')), edit.RecordType)
                except json.decoder.JSONDecodeError:
                    return Response({'detail': 'JSON syntax error'})
                if not record_serializer.is_valid():
                    return Response(record_serializer.errors)
                edit.Value = validated_data.get('Value')
                edit.save()
            elif edit.EditType == 'update':
                edit.Value = validated_data.get('Value')
                edit.save()
        return Response(EditSerializer(edit).data)
    return Response(edit_serializer.errors)


def get_record_serializer(data, record_type):
    if record_type == 'AHJ':
        return AHJSerializer(data=data)
    elif record_type == 'Address':
        return AddressSerializer(data=data)
    elif record_type == 'Location':
        return LocationSerializer(data=data)


def apply_edit(edit):
    if edit.EditType == 'create':
        serializer = get_record_serializer(json.loads(edit.Value), edit.RecordType)
        if serializer.is_valid():
            serializer.create(serializer.validated_data, edit)
    elif edit.EditType == 'update':
        # must check if record still exists
        record = get_record(edit.RecordID, edit.RecordType)
        if record is not None:
            # It was already checked when edit was created that FieldName is valid
            setattr(record, edit.FieldName, edit.Value)
            record.save()
            edit.save()
    elif edit.EditType == 'delete':
        record = get_record(edit.RecordID, edit.RecordType)
        if record is not None:
            record.delete()
        # Need to create edits to record deleting child objects
        edit.save()


def get_record(record_id, record_type):
    record = None
    if record_type == 'AHJ':
        record = AHJ.objects.filter(AHJID=record_id).first()
    else:
        record = apps.get_model('core', record_type).objects.filter(pk=record_type).first()
    return record
