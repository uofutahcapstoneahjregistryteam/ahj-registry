from rest_framework.test import APITestCase
from core.models import *
from core import views
from core import utils
from django.utils import timezone
from rest_framework import status
from .constants_test import *
import json
from .serializers import *


class EditTestCase(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create(email_address='super', password='super', is_superuser=True, is_active=True)
        self.owner = User.objects.create(email_address='owner', password='owner', is_active=True)
        self.user = User.objects.create(email_address='user', password='user', is_active=True)
        self.voter = User.objects.create(email_address='voter', password='voter', is_active=True)

    def become_super(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)

    def become_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='owner').key)

    def become_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='user').key)

    def become_voter(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='voter').key)

    def create_record_as_super(self, record_type, **kwargs):
        self.become_super()
        
        if record_type == 'AHJ':
            edit_create = EDIT_CREATE_AHJ
        elif record_type == 'Contact':
            edit_create = EDIT_CREATE_CONTACT(kwargs.get('parent_id', None))
        elif record_type == 'Address':
            edit_create = EDIT_CREATE_ADDRESS(kwargs.get('parent_id', None), kwargs.get('parent_type', None))
        elif record_type == 'Location':
            edit_create = EDIT_CREATE_LOCATION(kwargs.get('parent_id', None))
        elif record_type == 'EngineeringReviewRequirement':
            edit_create = EDIT_CREATE_ENG_REV_REQ(kwargs.get('parent_id', None))
        else:
            raise ValueError('TESTING_INVALID_RECORD_TYPE')

        return self.client.post(EDIT_SUBMIT_ENDPOINT, edit_create)

    def create_record_as_user(self, record_type, **kwargs):
        self.become_user()

        if record_type == 'AHJ':
            edit_create = EDIT_CREATE_AHJ
        elif record_type == 'Contact':
            edit_create = EDIT_CREATE_CONTACT(kwargs.get('parent_id', None))
        elif record_type == 'Address':
            edit_create = EDIT_CREATE_ADDRESS(kwargs.get('parent_id', None), kwargs.get('parent_type', None))
        elif record_type == 'Location':
            edit_create = EDIT_CREATE_LOCATION(kwargs.get('parent_id', None))
        elif record_type == 'EngineeringReviewRequirement':
            edit_create = EDIT_CREATE_ENG_REV_REQ(kwargs.get('parent_id', None))
        else:
            raise ValueError('TESTING_INVALID_RECORD_TYPE')

        return self.client.post(EDIT_SUBMIT_ENDPOINT, edit_create)

    def create_record_as_owner(self, record_type, **kwargs):
        self.become_owner()

        if record_type == 'AHJ':
            edit_create = EDIT_CREATE_AHJ
        elif record_type == 'Contact':
            edit_create = EDIT_CREATE_CONTACT(kwargs.get('parent_id', None))
        elif record_type == 'Address':
            edit_create = EDIT_CREATE_ADDRESS(kwargs.get('parent_id', None), kwargs.get('parent_type', None))
        elif record_type == 'Location':
            edit_create = EDIT_CREATE_LOCATION(kwargs.get('parent_id', None))
        elif record_type == 'EngineeringReviewRequirement':
            edit_create = EDIT_CREATE_ENG_REV_REQ(kwargs.get('parent_id', None))
        else:
            raise ValueError('TESTING_INVALID_RECORD_TYPE')

        return self.client.post(EDIT_SUBMIT_ENDPOINT, edit_create)

    """
    Test adding and removing AHJ owners
    """

    def test_add_owner_to_AHJ(self):
        response = self.create_record_as_super('AHJ')
        AHJID = response.json()['RecordID']
        self.client.get(AHJ_OWNER_ENDPOINT('add', self.owner.id, AHJID))

        self.assertTrue(self.owner.AHJ.filter(AHJID=AHJID).exists())
        self.assertTrue(AHJ.objects.filter(user__id=self.owner.id))

    def test_remove_owner_from_AHJ(self):
        response = self.create_record_as_super('AHJ')
        AHJID = response.json()['RecordID']
        self.client.get(AHJ_OWNER_ENDPOINT('add', self.owner.id, AHJID))
        self.client.get(AHJ_OWNER_ENDPOINT('remove', self.owner.id, AHJID))

        self.assertFalse(self.owner.AHJ.filter(AHJID=AHJID).exists())
        self.assertFalse(AHJ.objects.filter(user__id=self.owner.id))

    """
    Test creating records with Edit
    """

    def test_edit_create_AHJ_alone(self):
        response = self.create_record_as_super(record_type='AHJ')

        self.assertTrue(response.status_code == status.HTTP_201_CREATED)
        AHJID = response.json()['RecordID']

        self.assertTrue(AHJ.objects.filter(AHJID=AHJID).exists())

    def test_edit_create_Address(self):
        ahj_response = self.create_record_as_super(record_type='AHJ')
        AHJID = ahj_response.json()['RecordID']
        address_response = self.create_record_as_super('Address', parent_id=AHJID, parent_type='AHJ')

        self.assertTrue(address_response.status_code == status.HTTP_201_CREATED)

        address_id = address_response.json()['RecordID']

        self.assertTrue(Address.objects.filter(id=address_id).exists())
        self.assertTrue(Address.objects.filter(AHJ=AHJ.objects.get(AHJID=AHJID)).exists())

    def test_edit_create_Contact(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        contact_response = self.create_record_as_super('Contact', parent_id=AHJID)

        self.assertTrue(contact_response.status_code == status.HTTP_201_CREATED)

        contact_id = contact_response.json()['RecordID']

        self.assertTrue(Contact.objects.filter(id=contact_id).exists())
        self.assertTrue(Contact.objects.filter(AHJ=AHJ.objects.get(AHJID=AHJID)).exists())

    def test_edit_create_EngineeringReviewRequirement(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        eng_rev_req_response = self.create_record_as_super('EngineeringReviewRequirement', parent_id=AHJID)

        self.assertTrue(eng_rev_req_response.status_code == status.HTTP_201_CREATED)

        eng_rev_req_id = eng_rev_req_response.json()['RecordID']

        self.assertTrue(EngineeringReviewRequirement.objects.filter(id=eng_rev_req_id).exists())
        self.assertTrue(EngineeringReviewRequirement.objects.filter(AHJ=AHJ.objects.get(AHJID=AHJID)).exists())

    def test_edit_create_Address_Location(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        address_response = self.create_record_as_super('Address', parent_id=AHJID, parent_type='AHJ')
        address_id = address_response.json()['RecordID']
        location_response = self.create_record_as_super('Location', parent_id=address_id)

        self.assertTrue(location_response.status_code == status.HTTP_201_CREATED)

        location_id = location_response.json()['RecordID']

        self.assertTrue(Location.objects.filter(id=location_id).exists())
        self.assertTrue(Location.objects.filter(Address=Address.objects.get(id=address_id)).exists())

    def test_edit_create_Contact_Address(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        contact_response = self.create_record_as_super('Contact', parent_id=AHJID)
        contact_id = contact_response.json()['RecordID']
        address_response = self.create_record_as_super('Address', parent_id=contact_id, parent_type='Contact')

        self.assertTrue(address_response.status_code == status.HTTP_201_CREATED)

        address_id = address_response.json()['RecordID']

        self.assertTrue(Address.objects.filter(id=address_id).exists())
        self.assertTrue(Address.objects.filter(Contact=Contact.objects.get(id=contact_id)).exists())

    def test_edit_create_confirm_AHJ_alone(self):
        ahj_response = self.create_record_as_user('AHJ')
        AHJID = ahj_response.json()['RecordID']
        edit_id = ahj_response.json()['EditID']

        self.become_super()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        self.assertTrue(Edit.objects.get(pk=edit_id).IsConfirmed)
        self.assertTrue(AHJ.objects.filter(AHJID=AHJID).exists())

    def test_edit_create_reject_AHJ_alone(self):
        ahj_response = self.create_record_as_user('AHJ')
        AHJID = ahj_response.json()['RecordID']
        edit_id = ahj_response.json()['EditID']

        self.become_super()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'rejected'))

        self.assertFalse(Edit.objects.get(pk=edit_id).IsConfirmed)
        self.assertFalse(AHJ.objects.filter(AHJID=AHJID).exists())

    def test_edit_create_confirm_Address(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        address_response = self.create_record_as_user('Address', parent_id=AHJID, parent_type='AHJ')
        edit_id = address_response.json()['EditID']

        self.become_super()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        self.assertTrue(Edit.objects.get(pk=edit_id).IsConfirmed)

    def test_edit_create_reject_Address(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        address_response = self.create_record_as_user('Address', parent_id=AHJID, parent_type='AHJ')
        address_id = address_response.json()['RecordID']
        edit_id = address_response.json()['EditID']

        self.become_super()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'rejected'))

        self.assertFalse(Edit.objects.get(pk=edit_id).IsConfirmed)
        self.assertFalse(Address.objects.filter(id=address_id).exists())

    def test_edit_create_unconfirmed_parent_block_confirm_Address(self):
        ahj_response = self.create_record_as_user('AHJ')
        AHJID = ahj_response.json()['RecordID']
        address_response = self.create_record_as_user('Address', parent_id=AHJID, parent_type='AHJ')
        edit_id = address_response.json()['EditID']

        self.become_super()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        self.assertIsNone(Edit.objects.get(pk=edit_id).IsConfirmed)

    def test_edit_create_confirm_Contact(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        contact_response = self.create_record_as_user('Contact', parent_id=AHJID)
        edit_id = contact_response.json()['EditID']

        self.become_super()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        self.assertTrue(Edit.objects.get(pk=edit_id).IsConfirmed)

    def test_edit_create_reject_Contact(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        contact_response = self.create_record_as_user('Contact', parent_id=AHJID)
        contact_id = contact_response.json()['RecordID']
        edit_id = contact_response.json()['EditID']

        self.become_super()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'rejected'))

        self.assertFalse(Edit.objects.get(pk=edit_id).IsConfirmed)
        self.assertFalse(Contact.objects.filter(id=contact_id).exists())

    def test_edit_create_unconfirmed_parent_block_confirm_Contact(self):
        ahj_response = self.create_record_as_user('AHJ')
        AHJID = ahj_response.json()['RecordID']
        contact_response = self.create_record_as_user('Contact', parent_id=AHJID)
        edit_id = contact_response.json()['EditID']

        self.become_super()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        self.assertIsNone(Edit.objects.get(pk=edit_id).IsConfirmed)

    def test_edit_create_confirm_EngRevReq(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        eng_rev_req_response = self.create_record_as_user('EngineeringReviewRequirement', parent_id=AHJID)
        edit_id = eng_rev_req_response.json()['EditID']

        self.become_super()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        self.assertTrue(Edit.objects.get(pk=edit_id).IsConfirmed)

    def test_edit_create_reject_EngRevReq(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        eng_rev_req_response = self.create_record_as_user('EngineeringReviewRequirement', parent_id=AHJID)
        eng_rev_req_id = eng_rev_req_response.json()['RecordID']
        edit_id = eng_rev_req_response.json()['EditID']

        self.become_super()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'rejected'))

        self.assertFalse(Edit.objects.get(pk=edit_id).IsConfirmed)
        self.assertFalse(EngineeringReviewRequirement.objects.filter(id=eng_rev_req_id).exists())

    def test_edit_create_unconfirmed_parent_block_confirm_EngRevReq(self):
        ahj_response = self.create_record_as_user('AHJ')
        AHJID = ahj_response.json()['RecordID']
        contact_response = self.create_record_as_user('EngineeringReviewRequirement', parent_id=AHJID)
        edit_id = contact_response.json()['EditID']

        self.become_super()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        self.assertIsNone(Edit.objects.get(pk=edit_id).IsConfirmed)

    def test_edit_create_confirm_Contact_Address(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        contact_response = self.create_record_as_super('Contact', parent_id=AHJID)
        contact_id = contact_response.json()['RecordID']
        address_response = self.create_record_as_user('Address', parent_id=contact_id, parent_type='Contact')
        edit_id = address_response.json()['EditID']

        self.become_super()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        self.assertTrue(Edit.objects.get(pk=edit_id).IsConfirmed)

    def test_edit_create_reject_Contact_Address(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        contact_response = self.create_record_as_super('Contact', parent_id=AHJID)
        contact_id = contact_response.json()['RecordID']
        address_response = self.create_record_as_user('Address', parent_id=contact_id, parent_type='Contact')
        address_id = address_response.json()['RecordID']
        edit_id = address_response.json()['EditID']

        self.become_super()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'rejected'))

        self.assertFalse(Edit.objects.get(pk=edit_id).IsConfirmed)
        self.assertFalse(Address.objects.filter(id=address_id).exists())

    def test_edit_create_unconfirmed_parent_block_confirm_Contact_Address(self):
        ahj_response = self.create_record_as_user('AHJ')
        AHJID = ahj_response.json()['RecordID']
        contact_response = self.create_record_as_user('Contact', parent_id=AHJID)
        contact_id = contact_response.json()['RecordID']
        address_response = self.create_record_as_user('Address', parent_id=contact_id, parent_type='Contact')
        edit_id = address_response.json()['EditID']

        self.become_super()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        self.assertIsNone(Edit.objects.get(pk=edit_id).IsConfirmed)

    def test_edit_create_confirm_Address_Location(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        address_response = self.create_record_as_super('Address', parent_id=AHJID, parent_type='AHJ')
        address_id = address_response.json()['RecordID']
        location_response = self.create_record_as_user('Location', parent_id=address_id)
        edit_id = location_response.json()['EditID']

        self.become_super()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        self.assertTrue(Edit.objects.get(pk=edit_id).IsConfirmed)

    def test_edit_create_reject_Address_Location(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        address_response = self.create_record_as_super('Address', parent_id=AHJID, parent_type='AHJ')
        address_id = address_response.json()['RecordID']
        location_response = self.create_record_as_user('Location', parent_id=address_id)
        location_id = location_response.json()['RecordID']
        edit_id = location_response.json()['EditID']

        self.become_super()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'rejected'))

        self.assertFalse(Edit.objects.get(pk=edit_id).IsConfirmed)
        self.assertFalse(Location.objects.filter(id=location_id).exists())

    def test_edit_create_unconfirmed_parent_block_confirm_Address_Location(self):
        ahj_response = self.create_record_as_user('AHJ')
        AHJID = ahj_response.json()['RecordID']
        address_response = self.create_record_as_user('Address', parent_id=AHJID, parent_type='AHJ')
        address_id = address_response.json()['RecordID']
        location_response = self.create_record_as_user('Location', parent_id=address_id)
        edit_id = location_response.json()['EditID']

        self.become_super()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        self.assertIsNone(Edit.objects.get(pk=edit_id).IsConfirmed)

    def test_edit_create_AHJ_whole(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        ahj_address_response = self.create_record_as_super('Address', parent_id=AHJID, parent_type='AHJ')
        ahj_address_id = ahj_address_response.json()['RecordID']
        ahj_address_location_response = self.create_record_as_super('Location', parent_id=ahj_address_id)
        ahj_address_location_id = ahj_address_location_response.json()['RecordID']
        contact_response = self.create_record_as_super('Contact', parent_id=AHJID)
        contact_id = contact_response.json()['RecordID']
        contact_address_response = self.create_record_as_super('Address', parent_id=contact_id, parent_type='Contact')
        contact_address_id = contact_address_response.json()['RecordID']
        contact_address_location_response = self.create_record_as_super('Location', parent_id=contact_address_id)
        contact_address_location_id = contact_address_location_response.json()['RecordID']
        eng_rev_req_response = self.create_record_as_super('EngineeringReviewRequirement', parent_id=AHJID)
        eng_rev_req_id = eng_rev_req_response.json()['RecordID']

        self.assertTrue(AHJ.objects.filter(AHJID=AHJID).exists())

        self.assertTrue(Edit.objects.filter(RecordType='Address').filter(RecordID=ahj_address_id).exists())
        self.assertTrue(Address.objects.filter(id=ahj_address_id).exists())

        self.assertTrue(Edit.objects.filter(RecordType='Location').filter(RecordID=ahj_address_location_id).exists())
        self.assertTrue(Location.objects.filter(id=ahj_address_location_id).exists())

        self.assertTrue(Edit.objects.filter(RecordType='Contact').filter(RecordID=contact_id).exists())
        self.assertTrue(Contact.objects.filter(id=contact_id).exists())

        self.assertTrue(Edit.objects.filter(RecordType='Address').filter(RecordID=contact_address_id).exists())
        self.assertTrue(Address.objects.filter(id=contact_address_id).exists())

        self.assertTrue(Edit.objects.filter(RecordType='Location').filter(RecordID=contact_address_location_id).exists())
        self.assertTrue(Location.objects.filter(id=contact_address_location_id).exists())

        self.assertTrue(Edit.objects.filter(RecordType='EngineeringReviewRequirement').filter(RecordID=eng_rev_req_id).exists())
        self.assertTrue(EngineeringReviewRequirement.objects.filter(id=eng_rev_req_id).exists())

    def test_edit_create_reject_AHJ_whole(self):
        ahj_response = self.create_record_as_user('AHJ')
        AHJID = ahj_response.json()['RecordID']
        edit_id = ahj_response.json()['EditID']
        ahj_address_response = self.create_record_as_user('Address', parent_id=AHJID, parent_type='AHJ')
        ahj_address_id = ahj_address_response.json()['RecordID']
        ahj_address_location_response = self.create_record_as_user('Location', parent_id=ahj_address_id)
        ahj_address_location_id = ahj_address_location_response.json()['RecordID']
        contact_response = self.create_record_as_user('Contact', parent_id=AHJID)
        contact_id = contact_response.json()['RecordID']
        contact_address_response = self.create_record_as_user('Address', parent_id=contact_id, parent_type='Contact')
        contact_address_id = contact_address_response.json()['RecordID']
        contact_address_location_response = self.create_record_as_user('Location', parent_id=contact_address_id)
        contact_address_location_id = contact_address_location_response.json()['RecordID']
        eng_rev_req_response = self.create_record_as_user('EngineeringReviewRequirement', parent_id=AHJID)
        eng_rev_req_id = eng_rev_req_response.json()['RecordID']

        self.become_super()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'rejected'))

        self.assertFalse(Edit.objects.get(pk=edit_id).IsConfirmed)
        self.assertFalse(AHJ.objects.filter(AHJID=AHJID).exists())

        self.assertFalse(Edit.objects.filter(RecordType='Address').get(RecordID=ahj_address_id).IsConfirmed)
        self.assertFalse(Address.objects.filter(id=ahj_address_id).exists())

        self.assertFalse(Edit.objects.filter(RecordType='Location').get(RecordID=ahj_address_location_id).IsConfirmed)
        self.assertFalse(Location.objects.filter(id=ahj_address_location_id).exists())

        self.assertFalse(Edit.objects.filter(RecordType='Contact').get(RecordID=contact_id).IsConfirmed)
        self.assertFalse(Contact.objects.filter(id=contact_id).exists())

        self.assertFalse(Edit.objects.filter(RecordType='Address').get(RecordID=contact_address_id).IsConfirmed)
        self.assertFalse(Address.objects.filter(id=contact_address_id).exists())

        self.assertFalse(Edit.objects.filter(RecordType='Location').get(RecordID=contact_address_location_id).IsConfirmed)
        self.assertFalse(Location.objects.filter(id=contact_address_location_id).exists())

        self.assertFalse(Edit.objects.filter(RecordType='EngineeringReviewRequirement').get(RecordID=eng_rev_req_id).IsConfirmed)
        self.assertFalse(EngineeringReviewRequirement.objects.filter(id=eng_rev_req_id).exists())

    def test_edit_create_owner_confirm_Address(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        self.client.get(AHJ_OWNER_ENDPOINT('add', self.owner.id, AHJID))
        address_response = self.create_record_as_user('Address', parent_id=AHJID, parent_type='AHJ')
        edit_id = address_response.json()['EditID']

        self.become_owner()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        self.assertTrue(Edit.objects.get(pk=edit_id).IsConfirmed)

    def test_edit_create_owner_reject_Address(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        self.client.get(AHJ_OWNER_ENDPOINT('add', self.owner.id, AHJID))
        address_response = self.create_record_as_user('Address', parent_id=AHJID, parent_type='AHJ')
        address_id = address_response.json()['RecordID']
        edit_id = address_response.json()['EditID']

        self.become_owner()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'rejected'))

        self.assertFalse(Edit.objects.get(pk=edit_id).IsConfirmed)
        self.assertFalse(Address.objects.filter(id=address_id).exists())

    def test_edit_create_owner_unconfirmed_parent_block_confirm_Address(self):
        ahj_response = self.create_record_as_user('AHJ')
        AHJID = ahj_response.json()['RecordID']
        self.client.get(AHJ_OWNER_ENDPOINT('add', self.owner.id, AHJID))
        address_response = self.create_record_as_user('Address', parent_id=AHJID, parent_type='AHJ')
        edit_id = address_response.json()['EditID']

        self.become_owner()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        self.assertIsNone(Edit.objects.get(pk=edit_id).IsConfirmed)

    def test_edit_create_owner_confirm_Contact(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        self.client.get(AHJ_OWNER_ENDPOINT('add', self.owner.id, AHJID))
        contact_response = self.create_record_as_user('Contact', parent_id=AHJID)
        edit_id = contact_response.json()['EditID']

        self.become_owner()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        self.assertTrue(Edit.objects.get(pk=edit_id).IsConfirmed)

    def test_edit_create_owner_reject_Contact(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        self.client.get(AHJ_OWNER_ENDPOINT('add', self.owner.id, AHJID))
        contact_response = self.create_record_as_user('Contact', parent_id=AHJID)
        contact_id = contact_response.json()['RecordID']
        edit_id = contact_response.json()['EditID']

        self.become_owner()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'rejected'))

        self.assertFalse(Edit.objects.get(pk=edit_id).IsConfirmed)
        self.assertFalse(Contact.objects.filter(id=contact_id).exists())

    def test_edit_create_owner_unconfirmed_parent_block_confirm_Contact(self):
        ahj_response = self.create_record_as_user('AHJ')
        AHJID = ahj_response.json()['RecordID']
        self.client.get(AHJ_OWNER_ENDPOINT('add', self.owner.id, AHJID))
        contact_response = self.create_record_as_user('Contact', parent_id=AHJID)
        edit_id = contact_response.json()['EditID']

        self.become_owner()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        self.assertIsNone(Edit.objects.get(pk=edit_id).IsConfirmed)

    def test_edit_create_owner_confirm_EngRevReq(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        self.client.get(AHJ_OWNER_ENDPOINT('add', self.owner.id, AHJID))
        eng_rev_req_response = self.create_record_as_user('EngineeringReviewRequirement', parent_id=AHJID)
        edit_id = eng_rev_req_response.json()['EditID']

        self.become_owner()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        self.assertTrue(Edit.objects.get(pk=edit_id).IsConfirmed)

    def test_edit_create_owner_reject_EngRevReq(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        self.client.get(AHJ_OWNER_ENDPOINT('add', self.owner.id, AHJID))
        eng_rev_req_response = self.create_record_as_user('EngineeringReviewRequirement', parent_id=AHJID)
        eng_rev_req_id = eng_rev_req_response.json()['RecordID']
        edit_id = eng_rev_req_response.json()['EditID']

        self.become_owner()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'rejected'))

        self.assertFalse(Edit.objects.get(pk=edit_id).IsConfirmed)
        self.assertFalse(EngineeringReviewRequirement.objects.filter(id=eng_rev_req_id).exists())

    def test_edit_create_owner_unconfirmed_parent_block_confirm_EngRevReq(self):
        ahj_response = self.create_record_as_user('AHJ')
        AHJID = ahj_response.json()['RecordID']
        self.client.get(AHJ_OWNER_ENDPOINT('add', self.owner.id, AHJID))
        contact_response = self.create_record_as_user('EngineeringReviewRequirement', parent_id=AHJID)
        edit_id = contact_response.json()['EditID']

        self.become_owner()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        self.assertIsNone(Edit.objects.get(pk=edit_id).IsConfirmed)

    def test_edit_create_owner_confirm_Contact_Address(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        self.client.get(AHJ_OWNER_ENDPOINT('add', self.owner.id, AHJID))
        contact_response = self.create_record_as_super('Contact', parent_id=AHJID)
        contact_id = contact_response.json()['RecordID']
        address_response = self.create_record_as_user('Address', parent_id=contact_id, parent_type='Contact')
        edit_id = address_response.json()['EditID']

        self.become_owner()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        self.assertTrue(Edit.objects.get(pk=edit_id).IsConfirmed)

    def test_edit_create_owner_reject_Contact_Address(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        self.client.get(AHJ_OWNER_ENDPOINT('add', self.owner.id, AHJID))
        contact_response = self.create_record_as_super('Contact', parent_id=AHJID)
        contact_id = contact_response.json()['RecordID']
        address_response = self.create_record_as_user('Address', parent_id=contact_id, parent_type='Contact')
        address_id = address_response.json()['RecordID']
        edit_id = address_response.json()['EditID']

        self.become_owner()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'rejected'))

        self.assertFalse(Edit.objects.get(pk=edit_id).IsConfirmed)
        self.assertFalse(Address.objects.filter(id=address_id).exists())

    def test_edit_create_owner_unconfirmed_parent_block_confirm_Contact_Address(self):
        ahj_response = self.create_record_as_user('AHJ')
        AHJID = ahj_response.json()['RecordID']
        self.client.get(AHJ_OWNER_ENDPOINT('add', self.owner.id, AHJID))
        contact_response = self.create_record_as_user('Contact', parent_id=AHJID)
        contact_id = contact_response.json()['RecordID']
        address_response = self.create_record_as_user('Address', parent_id=contact_id, parent_type='Contact')
        edit_id = address_response.json()['EditID']

        self.become_owner()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        self.assertIsNone(Edit.objects.get(pk=edit_id).IsConfirmed)

    def test_edit_create_owner_confirm_Address_Location(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        self.client.get(AHJ_OWNER_ENDPOINT('add', self.owner.id, AHJID))
        address_response = self.create_record_as_super('Address', parent_id=AHJID, parent_type='AHJ')
        address_id = address_response.json()['RecordID']
        location_response = self.create_record_as_user('Location', parent_id=address_id)
        edit_id = location_response.json()['EditID']

        self.become_owner()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        self.assertTrue(Edit.objects.get(pk=edit_id).IsConfirmed)

    def test_edit_create_owner_reject_Address_Location(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        self.client.get(AHJ_OWNER_ENDPOINT('add', self.owner.id, AHJID))
        address_response = self.create_record_as_super('Address', parent_id=AHJID, parent_type='AHJ')
        address_id = address_response.json()['RecordID']
        location_response = self.create_record_as_user('Location', parent_id=address_id)
        location_id = location_response.json()['RecordID']
        edit_id = location_response.json()['EditID']

        self.become_owner()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'rejected'))

        self.assertFalse(Edit.objects.get(pk=edit_id).IsConfirmed)
        self.assertFalse(Location.objects.filter(id=location_id).exists())

    def test_edit_create_owner_unconfirmed_parent_block_confirm_Address_Location(self):
        ahj_response = self.create_record_as_user('AHJ')
        AHJID = ahj_response.json()['RecordID']
        self.client.get(AHJ_OWNER_ENDPOINT('add', self.owner.id, AHJID))
        address_response = self.create_record_as_user('Address', parent_id=AHJID, parent_type='AHJ')
        address_id = address_response.json()['RecordID']
        location_response = self.create_record_as_user('Location', parent_id=address_id)
        edit_id = location_response.json()['EditID']

        self.become_owner()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        self.assertIsNone(Edit.objects.get(pk=edit_id).IsConfirmed)

    def test_edit_create_owner_create_Address(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        self.client.get(AHJ_OWNER_ENDPOINT('add', self.owner.id, AHJID))
        address_response = self.create_record_as_owner('Address', parent_id=AHJID, parent_type='AHJ')
        edit_id = address_response.json()['EditID']

        self.assertTrue(Address.objects.filter(AHJ=AHJ.objects.get(AHJID=AHJID)).exists())
        self.assertTrue(Edit.objects.get(pk=edit_id).IsConfirmed)

    """
    Test deleting records with Edit
    """

    def test_edit_delete_AHJ_alone(self):
        ahj_response = self.create_record_as_super('AHJ')

        AHJID = ahj_response.json()['RecordID']

        delete_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(AHJID, 'AHJ'))

        self.assertTrue(delete_response.status_code == status.HTTP_201_CREATED)
        self.assertFalse(AHJ.objects.filter(AHJID=AHJID).exists())

    def test_edit_delete_reject_AHJ_alone(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        self.become_user()
        delete_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(AHJID, 'AHJ'))
        edit_id = delete_response.json()['EditID']

        self.become_super()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'rejected'))

        self.assertFalse(Edit.objects.get(pk=edit_id).IsConfirmed)
        self.assertTrue(AHJ.objects.filter(AHJID=AHJID).exists())

    def test_edit_delete_unconfirmed_record_block_delete_AHJ_alone(self):
        ahj_response = self.create_record_as_user('AHJ')
        AHJID = ahj_response.json()['RecordID']

        self.become_super()
        delete_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(AHJID, 'AHJ'))

        self.assertTrue(delete_response.status_code == status.HTTP_403_FORBIDDEN)
        self.assertTrue(AHJ.objects.filter(AHJID=AHJID).exists())

    def test_edit_delete_Address_from_AHJ(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        address_create_response = self.create_record_as_super('Address', parent_id=AHJID, parent_type='AHJ')
        address_id = address_create_response.json()['RecordID']

        delete_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(address_id, 'Address'))

        self.assertTrue(delete_response.status_code == status.HTTP_201_CREATED)
        self.assertFalse(Address.objects.filter(AHJ=AHJ.objects.get(AHJID=AHJID)).exists())

    def test_edit_delete_unconfirmed_record_block_delete_Address_from_AHJ(self):
        ahj_response = self.create_record_as_user('AHJ')
        AHJID = ahj_response.json()['RecordID']
        address_create_response = self.create_record_as_user('Address', parent_id=AHJID, parent_type='AHJ')
        address_id = address_create_response.json()['RecordID']

        self.become_super()
        delete_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(address_id, 'Address'))

        self.assertTrue(delete_response.status_code == status.HTTP_403_FORBIDDEN)
        self.assertTrue(Address.objects.filter(AHJ=AHJ.objects.get(AHJID=AHJID)).exists())

    def test_edit_delete_Contact_from_AHJ(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        contact_response = self.create_record_as_super('Contact', parent_id=AHJID)
        contact_id = contact_response.json()['RecordID']

        delete_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(contact_id, 'Contact'))

        self.assertTrue(delete_response.status_code == status.HTTP_201_CREATED)
        self.assertFalse(Contact.objects.filter(AHJ=AHJ.objects.get(AHJID=AHJID)).exists())

    def test_edit_delete_unconfirmed_record_block_delete_Contact_from_AHJ(self):
        ahj_response = self.create_record_as_user('AHJ')
        AHJID = ahj_response.json()['RecordID']
        contact_response = self.create_record_as_user('Contact', parent_id=AHJID)
        contact_id = contact_response.json()['RecordID']

        self.become_super()
        delete_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(contact_id, 'Contact'))

        self.assertTrue(delete_response.status_code == status.HTTP_403_FORBIDDEN)
        self.assertTrue(Contact.objects.filter(AHJ=AHJ.objects.get(AHJID=AHJID)).exists())

    def test_edit_delete_EngRevReq_from_AHJ(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        eng_rev_req_create_response = self.create_record_as_super('EngineeringReviewRequirement', parent_id=AHJID)
        eng_rev_req_id = eng_rev_req_create_response.json()['RecordID']

        delete_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(eng_rev_req_id, 'EngineeringReviewRequirement'))

        self.assertTrue(delete_response.status_code == status.HTTP_201_CREATED)
        self.assertFalse(EngineeringReviewRequirement.objects.filter(AHJ=AHJ.objects.get(AHJID=AHJID)).exists())

    def test_edit_delete_unconfirmed_record_block_delete_EngRevReq_from_AHJ(self):
        ahj_response = self.create_record_as_user('AHJ')
        AHJID = ahj_response.json()['RecordID']
        eng_rev_req_create_response = self.create_record_as_user('EngineeringReviewRequirement', parent_id=AHJID)
        eng_rev_req_id = eng_rev_req_create_response.json()['RecordID']

        self.become_super()
        delete_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(eng_rev_req_id, 'EngineeringReviewRequirement'))

        self.assertTrue(delete_response.status_code == status.HTTP_403_FORBIDDEN)
        self.assertTrue(EngineeringReviewRequirement.objects.filter(AHJ=AHJ.objects.get(AHJID=AHJID)).exists())

    def test_edit_delete_Address_from_Contact(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        contact_response = self.create_record_as_super('Contact', parent_id=AHJID)
        contact_id = contact_response.json()['RecordID']
        address_create_response = self.create_record_as_super('Address', parent_id=contact_id, parent_type='Contact')
        address_id = address_create_response.json()['RecordID']

        delete_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(address_id, 'Address'))

        self.assertTrue(delete_response.status_code == status.HTTP_201_CREATED)
        self.assertFalse(Address.objects.filter(Contact=Contact.objects.get(id=contact_id)).exists())

    def test_edit_delete_unconfirmed_record_block_delete_Address_from_Contact(self):
        ahj_response = self.create_record_as_user('AHJ')
        AHJID = ahj_response.json()['RecordID']
        contact_response = self.create_record_as_user('Contact', parent_id=AHJID)
        contact_id = contact_response.json()['RecordID']
        address_create_response = self.create_record_as_user('Address', parent_id=contact_id, parent_type='Contact')
        address_id = address_create_response.json()['RecordID']

        self.become_super()
        delete_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(address_id, 'Address'))

        self.assertTrue(delete_response.status_code == status.HTTP_403_FORBIDDEN)
        self.assertTrue(Address.objects.filter(Contact=Contact.objects.get(id=contact_id)).exists())

    def test_edit_delete_Location_from_Address(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        address_create_response = self.create_record_as_super('Address', parent_id=AHJID, parent_type='AHJ')
        address_id = address_create_response.json()['RecordID']
        location_create_response = self.create_record_as_super('Location', parent_id=address_id)
        location_id = location_create_response.json()['RecordID']

        delete_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(location_id, 'Location'))

        self.assertTrue(delete_response.status_code == status.HTTP_201_CREATED)
        self.assertFalse(Location.objects.filter(Address=Address.objects.get(id=address_id)).exists())

    def test_edit_delete_unconfirmed_record_block_delete_Location_from_Address(self):
        ahj_response = self.create_record_as_user('AHJ')
        AHJID = ahj_response.json()['RecordID']
        address_create_response = self.create_record_as_user('Address', parent_id=AHJID, parent_type='AHJ')
        address_id = address_create_response.json()['RecordID']
        location_create_response = self.create_record_as_user('Location', parent_id=address_id)
        location_id = location_create_response.json()['RecordID']

        self.become_super()
        delete_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(location_id, 'Location'))

        self.assertTrue(delete_response.status_code == status.HTTP_403_FORBIDDEN)
        self.assertTrue(Location.objects.filter(Address=Address.objects.get(id=address_id)).exists())

    def test_edit_delete_AHJ_whole(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        ahj_address_response = self.create_record_as_super('Address', parent_id=AHJID, parent_type='AHJ')
        ahj_address_id = ahj_address_response.json()['RecordID']
        ahj_address_location_response = self.create_record_as_super('Location', parent_id=ahj_address_id)
        ahj_address_location_id = ahj_address_location_response.json()['RecordID']
        contact_response = self.create_record_as_super('Contact', parent_id=AHJID)
        contact_id = contact_response.json()['RecordID']
        contact_address_response = self.create_record_as_super('Address', parent_id=contact_id, parent_type='Contact')
        contact_address_id = contact_address_response.json()['RecordID']
        contact_address_location_response = self.create_record_as_super('Location', parent_id=contact_address_id)
        contact_address_location_id = contact_address_location_response.json()['RecordID']
        eng_rev_req_response = self.create_record_as_super('EngineeringReviewRequirement', parent_id=AHJID)
        eng_rev_req_id = eng_rev_req_response.json()['RecordID']

        delete_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(AHJID, 'AHJ'))

        self.assertTrue(delete_response.status_code == status.HTTP_201_CREATED)

        self.assertFalse(AHJ.objects.filter(AHJID=AHJID).exists())

        self.assertTrue(Edit.objects.filter(RecordType='Address').filter(RecordID=ahj_address_id).exists())
        self.assertFalse(Address.objects.filter(id=ahj_address_id).exists())

        self.assertTrue(Edit.objects.filter(RecordType='Location').filter(RecordID=ahj_address_location_id).exists())
        self.assertFalse(Location.objects.filter(id=ahj_address_location_id).exists())

        self.assertTrue(Edit.objects.filter(RecordType='Contact').filter(RecordID=contact_id).exists())
        self.assertFalse(Contact.objects.filter(id=contact_id).exists())

        self.assertTrue(Edit.objects.filter(RecordType='Address').filter(RecordID=contact_address_id).exists())
        self.assertFalse(Address.objects.filter(id=contact_address_id).exists())

        self.assertTrue(Edit.objects.filter(RecordType='Location').filter(RecordID=contact_address_location_id).exists())
        self.assertFalse(Location.objects.filter(id=contact_address_location_id).exists())

        self.assertTrue(Edit.objects.filter(RecordType='EngineeringReviewRequirement').filter(RecordID=eng_rev_req_id).exists())
        self.assertFalse(EngineeringReviewRequirement.objects.filter(id=eng_rev_req_id).exists())

    def test_edit_delete_unconfirmed_record_block_delete_AHJ_whole(self):
        ahj_response = self.create_record_as_user('AHJ')
        AHJID = ahj_response.json()['RecordID']
        ahj_address_response = self.create_record_as_user('Address', parent_id=AHJID, parent_type='AHJ')
        ahj_address_id = ahj_address_response.json()['RecordID']
        ahj_address_location_response = self.create_record_as_user('Location', parent_id=ahj_address_id)
        ahj_address_location_id = ahj_address_location_response.json()['RecordID']
        contact_response = self.create_record_as_user('Contact', parent_id=AHJID)
        contact_id = contact_response.json()['RecordID']
        contact_address_response = self.create_record_as_user('Address', parent_id=contact_id, parent_type='Contact')
        contact_address_id = contact_address_response.json()['RecordID']
        contact_address_location_response = self.create_record_as_user('Location', parent_id=contact_address_id)
        contact_address_location_id = contact_address_location_response.json()['RecordID']
        eng_rev_req_response = self.create_record_as_user('EngineeringReviewRequirement', parent_id=AHJID)
        eng_rev_req_id = eng_rev_req_response.json()['RecordID']

        self.become_super()
        delete_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(AHJID, 'AHJ'))
        
        self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(ahj_address_id, 'Address'))
        self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(ahj_address_location_id, 'Location'))
        self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(contact_id, 'Contact'))
        self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(contact_address_id, 'Address'))
        self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(contact_address_location_id, 'Location'))
        self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(eng_rev_req_id, 'EngineeringReviewRequirement'))

        self.assertTrue(delete_response.status_code == status.HTTP_403_FORBIDDEN)

        self.assertTrue(AHJ.objects.filter(AHJID=AHJID).exists())

        self.assertFalse(Edit.objects.filter(RecordType='Address').filter(RecordID=ahj_address_id).filter(EditType='delete').exists())
        self.assertTrue(Address.objects.filter(id=ahj_address_id).exists())

        self.assertFalse(Edit.objects.filter(RecordType='Location').filter(RecordID=ahj_address_location_id).filter(EditType='delete').exists())
        self.assertTrue(Location.objects.filter(id=ahj_address_location_id).exists())

        self.assertFalse(Edit.objects.filter(RecordType='Contact').filter(RecordID=contact_id).filter(EditType='delete').exists())
        self.assertTrue(Contact.objects.filter(id=contact_id).exists())

        self.assertFalse(Edit.objects.filter(RecordType='Address').filter(RecordID=contact_address_id).filter(EditType='delete').exists())
        self.assertTrue(Address.objects.filter(id=contact_address_id).exists())

        self.assertFalse(Edit.objects.filter(RecordType='Location').filter(RecordID=contact_address_location_id).filter(EditType='delete').exists())
        self.assertTrue(Location.objects.filter(id=contact_address_location_id).exists())

        self.assertFalse(Edit.objects.filter(RecordType='EngineeringReviewRequirement').filter(RecordID=eng_rev_req_id).filter(EditType='delete').exists())
        self.assertTrue(EngineeringReviewRequirement.objects.filter(id=eng_rev_req_id).exists())

    """
    Test updating records with Edit
    """

    def test_edit_update_AHJ_CharField(self):
        ahj_response = self.create_record_as_super('AHJ')
        RecordID = ahj_response.json()['RecordID']
        RecordType = 'AHJ'
        FieldName = 'AHJName'
        Value = 'new_name'

        update_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(RecordID, RecordType, FieldName, Value))

        self.assertTrue(update_response.status_code == status.HTTP_201_CREATED)
        self.assertEqual(getattr(AHJ.objects.get(AHJID=RecordID), FieldName), Value)

    def test_edit_update_AHJ_TextField(self):
        ahj_response = self.create_record_as_super('AHJ')
        RecordID = ahj_response.json()['RecordID']
        RecordType = 'AHJ'
        FieldName = 'Description'
        Value = 'new_description'

        update_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(RecordID, RecordType, FieldName, Value))

        self.assertTrue(update_response.status_code == status.HTTP_201_CREATED)
        self.assertEqual(getattr(AHJ.objects.get(AHJID=RecordID), FieldName), Value)

    def test_edit_update_AHJ_ChoiceField(self):
        ahj_response = self.create_record_as_super('AHJ')
        RecordID = ahj_response.json()['RecordID']
        RecordType = 'AHJ'
        FieldName = 'BuildingCode'
        Value = '2021IBC'

        update_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(RecordID, RecordType, FieldName, Value))

        self.assertTrue(update_response.status_code == status.HTTP_201_CREATED)
        self.assertEqual(getattr(AHJ.objects.get(AHJID=RecordID), FieldName), Value)

    def test_edit_update_AHJ_ChoiceField_not_choice(self):
        ahj_response = self.create_record_as_super('AHJ')
        RecordID = ahj_response.json()['RecordID']
        RecordType = 'AHJ'
        FieldName = 'BuildingCode'
        Value = 'noodles'

        update_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(RecordID, RecordType, FieldName, Value))

        self.assertTrue(update_response.status_code == status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(getattr(AHJ.objects.get(AHJID=RecordID), FieldName), Value)

    def test_edit_update_Location_DecimalField(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        address_response = self.create_record_as_super('Address', parent_id=AHJID, parent_type='AHJ')
        address_id = address_response.json()['RecordID']
        location_response = self.create_record_as_super('Location', parent_id=address_id)
        RecordID = location_response.json()['RecordID']
        RecordType = 'Location'
        FieldName = 'Longitude'
        Value = 90

        update_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(RecordID, RecordType, FieldName, Value))

        self.assertTrue(update_response.status_code == status.HTTP_201_CREATED)
        self.assertEqual(getattr(Location.objects.get(id=RecordID), FieldName), Value)

    def test_edit_update_Location_DecimalField_not_decimal(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        address_response = self.create_record_as_super('Address', parent_id=AHJID, parent_type='AHJ')
        address_id = address_response.json()['RecordID']
        location_response = self.create_record_as_super('Location', parent_id=address_id)
        RecordID = location_response.json()['RecordID']
        RecordType = 'Location'
        FieldName = 'Longitude'
        Value = 'cookies'

        update_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(RecordID, RecordType, FieldName, Value))

        self.assertTrue(update_response.status_code == status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(getattr(Location.objects.get(pk=RecordID), FieldName), Value)

    def test_edit_update_Location_DecimalField_field_validation_not_in_range(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        address_response = self.create_record_as_super('Address', parent_id=AHJID, parent_type='AHJ')
        address_id = address_response.json()['RecordID']
        location_response = self.create_record_as_super('Location', parent_id=address_id)
        RecordID = location_response.json()['RecordID']
        RecordType = 'Location'
        FieldName = 'Longitude'
        Value = -200

        update_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(RecordID, RecordType, FieldName, Value))

        self.assertTrue(update_response.status_code == status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(getattr(Location.objects.get(pk=RecordID), FieldName), Value)

    def test_edit_update_same_value_blocked(self):
        ahj_response = self.create_record_as_super('AHJ')
        RecordID = ahj_response.json()['RecordID']
        RecordType = 'AHJ'
        FieldName = 'AHJName'
        Value = 'name'

        self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(RecordID, RecordType, FieldName, Value))
        update_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(RecordID, RecordType, FieldName, Value))

        self.assertTrue(update_response.status_code == status.HTTP_400_BAD_REQUEST)

    def test_edit_update_already_existing_unconfirmed_same_value_blocked(self):
        ahj_response = self.create_record_as_super('AHJ')
        RecordID = ahj_response.json()['RecordID']
        RecordType = 'AHJ'
        FieldName = 'AHJName'
        Value = 'name'

        self.become_user()
        self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(RecordID, RecordType, FieldName, Value))

        self.become_super()
        update_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(RecordID, RecordType, FieldName, Value))

        self.assertTrue(update_response.status_code == status.HTTP_400_BAD_REQUEST)

    """
    Test voting on edits
    """

    def test_upvote(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        self.become_user()
        update_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(AHJID, 'AHJ', 'AHJName', 'name'))
        edit_id = update_response.json()['EditID']
        self.become_voter()
        self.client.get(EDIT_DETAIL_ENDPOINT_VOTE(edit_id, 'upvote'))

        edit = Edit.objects.get(pk=edit_id)
        self.assertTrue(Vote.objects.filter(Edit=edit).exists())
        self.assertEqual(edit.VoteRating, 1)

    def test_downvote(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        self.become_user()
        update_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(AHJID, 'AHJ', 'AHJName', 'name'))
        edit_id = update_response.json()['EditID']
        self.become_voter()
        self.client.get(EDIT_DETAIL_ENDPOINT_VOTE(edit_id, 'downvote'))

        edit = Edit.objects.get(pk=edit_id)
        self.assertTrue(Vote.objects.filter(Edit=edit).exists())
        self.assertEqual(edit.VoteRating, -1)

    def test_cancel_vote(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        self.become_user()
        update_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(AHJID, 'AHJ', 'AHJName', 'name'))
        edit_id = update_response.json()['EditID']
        self.become_voter()
        self.client.get(EDIT_DETAIL_ENDPOINT_VOTE(edit_id, 'upvote'))

        self.assertTrue(Vote.objects.filter(Edit=Edit.objects.get(pk=edit_id)).exists())

        self.client.get(EDIT_DETAIL_ENDPOINT_VOTE(edit_id, 'none'))
        self.assertFalse(Vote.objects.filter(Edit=Edit.objects.get(pk=edit_id)).exists())
        self.assertEqual(Edit.objects.get(pk=edit_id).VoteRating, 0)

    def test_if_never_voted_cant_cancel_vote(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        self.become_user()
        update_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(AHJID, 'AHJ', 'AHJName', 'name'))
        edit_id = update_response.json()['EditID']
        self.client.get(EDIT_DETAIL_ENDPOINT_VOTE(edit_id, 'none'))

        self.assertFalse(Vote.objects.filter(Edit=Edit.objects.get(pk=edit_id)).exists())
        self.assertEqual(Edit.objects.get(pk=edit_id).VoteRating, 0)

    def test_cant_vote_on_own_edit(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        self.become_user()
        update_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(AHJID, 'AHJ', 'AHJName', 'name'))
        edit_id = update_response.json()['EditID']

        self.client.get(EDIT_DETAIL_ENDPOINT_VOTE(edit_id, 'upvote'))
        self.assertFalse(Vote.objects.filter(Edit=Edit.objects.get(pk=edit_id)).exists())
        self.assertEqual(Edit.objects.get(pk=edit_id).VoteRating, 0)

        self.client.get(EDIT_DETAIL_ENDPOINT_VOTE(edit_id, 'downvote'))
        self.assertFalse(Vote.objects.filter(Edit=Edit.objects.get(pk=edit_id)).exists())
        self.assertEqual(Edit.objects.get(pk=edit_id).VoteRating, 0)

        self.client.get(EDIT_DETAIL_ENDPOINT_VOTE(edit_id, 'none'))
        self.assertFalse(Vote.objects.filter(Edit=Edit.objects.get(pk=edit_id)).exists())
        self.assertEqual(Edit.objects.get(pk=edit_id).VoteRating, 0)

    def test_cant_vote_on_confirmed_edit(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        update_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(AHJID, 'AHJ', 'AHJName', 'name'))
        edit_id = update_response.json()['EditID']
        self.become_voter()
        self.client.get(EDIT_DETAIL_ENDPOINT_VOTE(edit_id, 'upvote'))

        self.assertEqual(Edit.objects.get(pk=edit_id).VoteRating, 0)

    """
    Test API view modes
    """

    def test_view_detail_latest(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(AHJID, 'AHJ', 'AHJName', 'oldname'))
        self.become_user()
        self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(AHJID, 'AHJ', 'AHJName', 'newname'))

        ahj_response = self.client.get(AHJ_DETAIL_ENDPOINT(AHJID, ''))
        AHJName = ahj_response.json()['AHJName']['Value']

        self.assertEqual(AHJName, 'newname')

    def test_view_detail_confirmed(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(AHJID, 'AHJ', 'AHJName', 'oldname'))
        self.become_user()
        self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(AHJID, 'AHJ', 'AHJName', 'newname'))

        ahj_response = self.client.get(AHJ_DETAIL_ENDPOINT(AHJID, 'confirmed'))
        AHJName = ahj_response.json()['AHJName']['Value']

        self.assertEqual(AHJName, 'oldname')

    def test_view_detail_unconfirmed_highest_voted(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        self.become_user()
        self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(AHJID, 'AHJ', 'AHJName', 'oldname'))
        update_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(AHJID, 'AHJ', 'AHJName', 'newname'))
        edit_id = update_response.json()['EditID']
        self.client.get(EDIT_DETAIL_ENDPOINT_VOTE(edit_id, 'upvote'))

        ahj_response = self.client.get(AHJ_DETAIL_ENDPOINT(AHJID, 'highest_voted'))
        AHJName = ahj_response.json()['AHJName']['Value']

        self.assertEqual(AHJName, 'newname')

    def test_view_detail_unconfirmed_highest_voted_one_confirmed(self):
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        self.become_user()
        update_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(AHJID, 'AHJ', 'AHJName', 'oldname'))
        edit_id = update_response.json()['EditID']
        self.become_voter()
        self.client.get(EDIT_DETAIL_ENDPOINT_VOTE(edit_id, 'upvote'))
        self.become_super()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))
        self.become_user()
        self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(AHJID, 'AHJ', 'AHJName', 'newname'))

        ahj_response = self.client.get(AHJ_DETAIL_ENDPOINT(AHJID, 'highest_voted'))
        AHJName = ahj_response.json()['AHJName']['Value']

        self.assertEqual(AHJName, 'newname')

    def test_view_detail_unconfirmed_highest_voted_no_unconfirmed_return_latest_confirmed(self):
        AHJ.objects.all().delete()
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        update_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(AHJID, 'AHJ', 'AHJName', 'oldname'))
        edit_id = update_response.json()['EditID']
        self.become_voter()
        self.client.get(EDIT_DETAIL_ENDPOINT_VOTE(edit_id, 'upvote'))
        self.become_super()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))
        self.become_user()
        update_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(AHJID, 'AHJ', 'AHJName', 'newname'))
        edit_id = update_response.json()['EditID']
        self.become_super()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        ahj_response = self.client.get(AHJ_DETAIL_ENDPOINT(AHJID, 'highest_voted'))
        AHJName = ahj_response.json()['AHJName']['Value']

        self.assertEqual(AHJName, 'newname')

    def test_view_list_latest(self):
        AHJ.objects.all().delete()
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(AHJID, 'AHJ', 'AHJName', 'oldname'))
        self.become_user()
        self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(AHJID, 'AHJ', 'AHJName', 'newname'))

        ahj_response = self.client.get(AHJ_LIST_ENDPOINT(''))
        AHJName = ahj_response.json()['results'][0]['AHJName']['Value']

        self.assertEqual(AHJName, 'newname')

    def test_view_list_confirmed(self):
        AHJ.objects.all().delete()
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(AHJID, 'AHJ', 'AHJName', 'oldname'))
        self.become_user()
        self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(AHJID, 'AHJ', 'AHJName', 'newname'))

        ahj_response = self.client.get(AHJ_LIST_ENDPOINT('confirmed'))
        AHJName = ahj_response.json()['results'][0]['AHJName']['Value']

        self.assertEqual(AHJName, 'oldname')

    def test_view_list_unconfirmed_highest_voted(self):
        AHJ.objects.all().delete()
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        self.become_user()
        self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(AHJID, 'AHJ', 'AHJName', 'oldname'))
        update_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(AHJID, 'AHJ', 'AHJName', 'newname'))
        edit_id = update_response.json()['EditID']
        self.client.get(EDIT_DETAIL_ENDPOINT_VOTE(edit_id, 'upvote'))

        ahj_response = self.client.get(AHJ_LIST_ENDPOINT('highest_voted'))
        AHJName = ahj_response.json()['results'][0]['AHJName']['Value']

        self.assertEqual(AHJName, 'newname')

    def test_view_list_unconfirmed_highest_voted_one_confirmed(self):
        AHJ.objects.all().delete()
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        self.become_user()
        update_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(AHJID, 'AHJ', 'AHJName', 'oldname'))
        edit_id = update_response.json()['EditID']
        self.become_voter()
        self.client.get(EDIT_DETAIL_ENDPOINT_VOTE(edit_id, 'upvote'))
        self.become_super()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))
        self.become_user()
        self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(AHJID, 'AHJ', 'AHJName', 'newname'))

        ahj_response = self.client.get(AHJ_LIST_ENDPOINT('highest_voted'))
        AHJName = ahj_response.json()['results'][0]['AHJName']['Value']

        self.assertEqual(AHJName, 'newname')

    def test_view_list_unconfirmed_highest_voted_no_unconfirmed_return_latest_confirmed(self):
        AHJ.objects.all().delete()
        ahj_response = self.create_record_as_super('AHJ')
        AHJID = ahj_response.json()['RecordID']
        update_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(AHJID, 'AHJ', 'AHJName', 'oldname'))
        edit_id = update_response.json()['EditID']
        self.become_voter()
        self.client.get(EDIT_DETAIL_ENDPOINT_VOTE(edit_id, 'upvote'))
        self.become_super()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))
        self.become_user()
        update_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(AHJID, 'AHJ', 'AHJName', 'newname'))
        edit_id = update_response.json()['EditID']
        self.become_super()
        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        ahj_response = self.client.get(AHJ_LIST_ENDPOINT('highest_voted'))
        AHJName = ahj_response.json()['results'][0]['AHJName']['Value']

        self.assertEqual(AHJName, 'newname')
