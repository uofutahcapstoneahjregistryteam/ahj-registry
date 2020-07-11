from django.test import TestCase
from core.models import *
from core.utils import *
from django.utils import timezone
from .example_ob_json import *
import json
from .serializers import *


class EditTestCase(TestCase):
    def setUp(self):
        AHJ.objects.create(AHJName='before', BuildingCode='2021IBC')

    def test_create_edit_AHJ_only(self):
        edit = Edit.objects.create(RecordType='AHJ', EditType='create', Value=AHJ_ONLY, ModifyingUserID=1,
                                   ModifiedDate=timezone.now())
        apply_edit(edit)
        self.assertTrue(AHJ.objects.filter(AHJID=edit.RecordID).exists())
        created_ahj = AHJ.objects.get(AHJID=edit.RecordID)
        added_create_edits = Edit.objects.filter(RecordID=created_ahj.AHJID).exclude(EditType='create')

        # Number of fields excluding AHJID, Address, Contacts, and EngineeringReviewRequirements
        self.assertTrue(len(added_create_edits), 14)
        for e in added_create_edits:
            self.assertTrue(e.Value, getattr(created_ahj, e.FieldName))

    def test_create_edit_AHJ_Address(self):
        edit = Edit.objects.create(RecordType='AHJ', EditType='create', Value=AHJ_ADDRESS, ModifyingUserID=1,
                                   ModifiedDate=timezone.now())
        apply_edit(edit)
        self.assertTrue(AHJ.objects.filter(AHJID=edit.RecordID).exists())
        self.assertTrue(Address.objects.filter(AHJ=AHJ.objects.get(AHJID=edit.RecordID)))
        created_address = Address.objects.get(AHJ=AHJ.objects.get(AHJID=edit.RecordID))
        added_create_edits = Edit.objects.filter(RecordID=created_address.id).exclude(EditType='create')

        # Number of fields excluding Location
        self.assertTrue(len(added_create_edits), 10)
        for e in added_create_edits:
            self.assertTrue(e.Value, getattr(created_address, e.FieldName))

    def test_create_edit_AHJ_Address_Location(self):
        edit = Edit.objects.create(RecordType='AHJ', EditType='create', Value=AHJ_ADDRESS_LOCATION, ModifyingUserID=1,
                                   ModifiedDate=timezone.now())
        apply_edit(edit)
        self.assertTrue(AHJ.objects.filter(AHJID=edit.RecordID).exists())
        self.assertTrue(Address.objects.filter(AHJ=AHJ.objects.get(AHJID=edit.RecordID)).exists())
        self.assertTrue(Location.objects.filter(Address=Address.objects.get(AHJ=AHJ.objects.get(AHJID=edit.RecordID))).exists())
        created_location = Location.objects.get(Address=Address.objects.get(AHJ=AHJ.objects.get(AHJID=edit.RecordID)))
        added_create_edits = Edit.objects.filter(RecordID=created_location.id).exclude(EditType='create')

        # Number of fields excluding Location
        self.assertTrue(len(added_create_edits), 7)
        for e in added_create_edits:
            self.assertTrue(e.Value, getattr(created_location, e.FieldName))

    def test_update_edit_AHJ_AHJName(self):
        edit = Edit.objects.create(RecordID=AHJ.objects.get(AHJName='before').AHJID, RecordType='AHJ', EditType='update',
                                   FieldName='AHJName', Value='after', ModifyingUserID=1, ModifiedDate=timezone.now())
        apply_edit(edit)
        self.assertEqual(AHJ.objects.get(AHJID=edit.RecordID).AHJName, edit.Value)

    # def test_update_edit_AHJ_BuildingCode_invalid_value(self):
    #     edit = Edit.objects.create(RecordID=AHJ.objects.get(AHJName='before').AHJID, RecordType='AHJ', EditType='update',
    #                                FieldName='BuildingCode', Value='invalid', ModifyingUserID=1, ModifiedDate=timezone.now())
    #     apply_edit(edit)
    #     self.assertNotEqual(AHJ.objects.get(AHJID=edit.RecordID).BuildingCode, edit.Value)

    def test_delete_edit_AHJ_only(self):
        create = Edit.objects.create(RecordType='AHJ', EditType='create', Value=AHJ_ONLY, ModifyingUserID=1,
                                     ModifiedDate=timezone.now())
        apply_edit(create)
        delete = Edit.objects.create(RecordID=create.RecordID, RecordType='AHJ', EditType='delete', ModifyingUserID=1, ModifiedDate=timezone.now())
        apply_edit(delete)
        self.assertFalse(AHJ.objects.filter(AHJID=delete.RecordID).exists())

    def test_delete_edit_AHJ_Address(self):
        create = Edit.objects.create(RecordType='AHJ', EditType='create', Value=AHJ_ADDRESS, ModifyingUserID=1,
                                     ModifiedDate=timezone.now())
        apply_edit(create)
        address = Address.objects.get(AHJ=AHJ.objects.get(AHJID=create.RecordID))
        delete = Edit.objects.create(RecordID=create.RecordID, RecordType='AHJ', EditType='delete', ModifyingUserID=1, ModifiedDate=timezone.now())
        apply_edit(delete)
        self.assertFalse(AHJ.objects.filter(AHJID=delete.RecordID).exists())
        self.assertFalse(Address.objects.filter(id=address.id).exists())
        self.assertTrue(Edit.objects.filter(RecordID=address.id).exists())

    def test_delete_edit_AHJ_Address_Location(self):
        create = Edit.objects.create(RecordType='AHJ', EditType='create', Value=AHJ_ADDRESS_LOCATION, ModifyingUserID=1,
                                     ModifiedDate=timezone.now())
        apply_edit(create)
        address = Address.objects.get(AHJ=AHJ.objects.get(AHJID=create.RecordID))
        location = Location.objects.get(Address=address)
        delete = Edit.objects.create(RecordID=create.RecordID, RecordType='AHJ', EditType='delete', ModifyingUserID=1, ModifiedDate=timezone.now())
        apply_edit(delete)
        self.assertFalse(AHJ.objects.filter(AHJID=delete.RecordID).exists())
        self.assertFalse(Address.objects.filter(id=address.id).exists())
        self.assertFalse(Location.objects.filter(id=location.id).exists())
        self.assertTrue(Edit.objects.filter(RecordID=address.id).exists())
        self.assertTrue(Edit.objects.filter(RecordID=location.id).exists())
