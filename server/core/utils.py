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

        if not edit.validate_RecordType():
            return Response({'detail': 'Invalid record type'})

        edit.ModifyingUserID = request.user.id

        if edit.EditType == 'create':
            if edit.RecordType != 'AHJ':
                if edit.ParentID == '' or not edit.validate_ParentRecordType():
                    return Response({'detail': 'Invalid parent record type'})
            edit.create_record()
        elif edit.EditType == 'update':
            if edit.RecordID == '':
                return Response({'detail': 'No record ID was given'})
            if edit.Value == '':
                return Response({'detail': 'No value was given'})
            if not edit.validate_FieldName():
                return Response({'detail': 'Cannot submit edit for given field name.'})
            edit.PreviousValue = getattr(edit.get_record(), edit.FieldName)
        elif edit.EditType == 'delete':
            if not check_record_edit_create_confirmed(edit.get_record()):
                return Response({'detail': 'Cannot make delete request records awaiting confirmation'})

        if request.user.is_superuser or request.user.id == edit.get_record_owner_id():
            edit.accept(request.user.id)
            return Response(EditSerializer(edit).data)
        else:
            edit.save()
            return Response(EditSerializer(edit).data)
    return Response(edit_serializer.errors)


def set_edit(request, pk):
    edit = Edit.objects.filter(pk=pk).first()
    if edit is None:
        return Response({'detail': 'Edit not found'})
    user = request.user
    confirm_status = request.GET.get('confirm', '')
    if confirm_status != '':
        return set_edit_status(confirm_status, user, edit)
    vote_status = request.Get.get('vote', '')
    if vote_status != '':
        return set_edit_vote(vote_status, user, edit)
    return Response(EditSerializer(edit).data)


def set_edit_status(confirm_status, user, edit):
    if edit.IsConfirmed is not None:
        return Response({'detail': 'Edit has already been processed. Please submit another edit.'})
    if user.is_superuser or user.id == edit.get_record_owner_id():
        if confirm_status == 'accepted':
            edit.accept(user_id=user.id)
        elif confirm_status == 'rejected':
            edit.reject(user_id=user.id)
        return Response(EditSerializer(edit).data)
    else:
        return Response({'detail': 'Could not confirm edit'})


def set_edit_vote(vote_status, user, edit):
    return Response({'detail': 'voted'})

