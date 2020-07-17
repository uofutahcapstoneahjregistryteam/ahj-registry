from rest_framework.test import APITestCase
from core.models import *
from core import views
from core import utils
from django.utils import timezone
from .constants_test import *
import json
from .serializers import *


class EditTestCase(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create(email_address='super', password='super', is_superuser=True, is_active=True)
        self.user = User.objects.create(email_address='user', password='user', is_active=True)

    """
    Test creating records with Edit
    """

    def test_edit_create_AHJ_alone(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)
        response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)

        self.assertTrue(response.status_code == 200)

        AHJID = response.json()['RecordID']

        self.assertTrue(AHJ.objects.filter(AHJID=AHJID).exists())

    def test_edit_create_Address(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        address_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ADDRESS(AHJID, 'AHJ'))

        self.assertTrue(address_response.status_code == 200)

        address_id = address_response.json()['RecordID']

        self.assertTrue(Address.objects.filter(id=address_id).exists())
        self.assertTrue(Address.objects.filter(AHJ=AHJ.objects.get(AHJID=AHJID)).exists())

    def test_edit_create_Contact(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        contact_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_CONTACT(AHJID))

        self.assertTrue(contact_response.status_code == 200)

        contact_id = contact_response.json()['RecordID']

        self.assertTrue(Contact.objects.filter(id=contact_id).exists())
        self.assertTrue(Contact.objects.filter(AHJ=AHJ.objects.get(AHJID=AHJID)).exists())

    def test_edit_create_EngineeringReviewRequirement(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        eng_rev_req_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ENG_REV_REQ(AHJID))

        self.assertTrue(eng_rev_req_response.status_code == 200)

        eng_rev_req_id = eng_rev_req_response.json()['RecordID']

        self.assertTrue(EngineeringReviewRequirement.objects.filter(id=eng_rev_req_id).exists())
        self.assertTrue(EngineeringReviewRequirement.objects.filter(AHJ=AHJ.objects.get(AHJID=AHJID)).exists())

    def test_edit_create_Address_Location(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        address_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ADDRESS(AHJID, 'AHJ'))
        address_id = address_response.json()['RecordID']
        locaiton_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_LOCATION(address_id))

        self.assertTrue(locaiton_response.status_code == 200)

        location_id = locaiton_response.json()['RecordID']

        self.assertTrue(Location.objects.filter(id=location_id).exists())
        self.assertTrue(Location.objects.filter(Address=Address.objects.get(id=address_id)).exists())

    def test_edit_create_Contact_Address(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        contact_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_CONTACT(AHJID))
        contact_id = contact_response.json()['RecordID']
        address_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ADDRESS(contact_id, 'Contact'))

        self.assertTrue(address_response.status_code == 200)

        address_id = address_response.json()['RecordID']

        self.assertTrue(Address.objects.filter(id=address_id).exists())
        self.assertTrue(Address.objects.filter(Contact=Contact.objects.get(id=contact_id)).exists())

    def test_edit_create_confirm_AHJ_alone(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='user').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        edit_id = ahj_response.json()['id']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)

        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        self.assertTrue(Edit.objects.get(pk=edit_id).IsConfirmed)
        self.assertTrue(AHJ.objects.filter(AHJID=AHJID).exists())

    def test_edit_create_reject_AHJ_alone(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='user').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        edit_id = ahj_response.json()['id']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)

        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'rejected'))

        self.assertFalse(Edit.objects.get(pk=edit_id).IsConfirmed)
        self.assertFalse(AHJ.objects.filter(AHJID=AHJID).exists())

    def test_edit_create_confirm_Address(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='user').key)
        address_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ADDRESS(AHJID, 'AHJ'))
        edit_id = address_response.json()['EditID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)

        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        self.assertTrue(Edit.objects.get(pk=edit_id).IsConfirmed)

    def test_edit_create_reject_Address(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='user').key)
        address_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ADDRESS(AHJID, 'AHJ'))
        address_id = address_response.json()['RecordID']
        edit_id = address_response.json()['EditID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)

        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'rejected'))

        self.assertFalse(Edit.objects.get(pk=edit_id).IsConfirmed)
        self.assertFalse(Address.objects.filter(id=address_id).exists())

    def test_edit_create_unconfirmed_parent_block_confirm_Address(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='user').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        address_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ADDRESS(AHJID, 'AHJ'))
        edit_id = address_response.json()['EditID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)

        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        self.assertIsNone(Edit.objects.get(pk=edit_id).IsConfirmed)

    def test_edit_create_confirm_Contact(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='user').key)
        contact_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_CONTACT(AHJID))
        edit_id = contact_response.json()['EditID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)

        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        self.assertTrue(Edit.objects.get(pk=edit_id).IsConfirmed)

    def test_edit_create_reject_Contact(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='user').key)
        contact_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_CONTACT(AHJID))
        contact_id = contact_response.json()['RecordID']
        edit_id = contact_response.json()['EditID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)

        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'rejected'))

        self.assertFalse(Edit.objects.get(pk=edit_id).IsConfirmed)
        self.assertFalse(Contact.objects.filter(id=contact_id).exists())

    def test_edit_create_unconfirmed_parent_block_confirm_Contact(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='user').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        contact_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_CONTACT(AHJID))
        edit_id = contact_response.json()['EditID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)

        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        self.assertIsNone(Edit.objects.get(pk=edit_id).IsConfirmed)

    def test_edit_create_confirm_EngRevReq(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='user').key)
        eng_rev_req_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ENG_REV_REQ(AHJID))
        edit_id = eng_rev_req_response.json()['EditID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)

        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        self.assertTrue(Edit.objects.get(pk=edit_id).IsConfirmed)

    def test_edit_create_reject_EngRevReq(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='user').key)
        eng_rev_req_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ENG_REV_REQ(AHJID))
        eng_rev_req_id = eng_rev_req_response.json()['RecordID']
        edit_id = eng_rev_req_response.json()['EditID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)

        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'rejected'))

        self.assertFalse(Edit.objects.get(pk=edit_id).IsConfirmed)
        self.assertFalse(EngineeringReviewRequirement.objects.filter(id=eng_rev_req_id).exists())

    def test_edit_create_unconfirmed_parent_block_confirm_EngRevReq(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='user').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        contact_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ENG_REV_REQ(AHJID))
        edit_id = contact_response.json()['EditID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)

        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        self.assertIsNone(Edit.objects.get(pk=edit_id).IsConfirmed)

    def test_edit_create_confirm_Contact_Address(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        contact_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_CONTACT(AHJID))
        contact_id = contact_response.json()['RecordID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='user').key)
        address_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ADDRESS(contact_id, 'Contact'))
        edit_id = address_response.json()['EditID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)

        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        self.assertTrue(Edit.objects.get(pk=edit_id).IsConfirmed)

    def test_edit_create_reject_Contact_Address(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        contact_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_CONTACT(AHJID))
        contact_id = contact_response.json()['RecordID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='user').key)
        address_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ADDRESS(contact_id, 'Contact'))
        address_id = address_response.json()['RecordID']
        edit_id = address_response.json()['EditID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)

        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'rejected'))

        self.assertFalse(Edit.objects.get(pk=edit_id).IsConfirmed)
        self.assertFalse(Address.objects.filter(id=address_id).exists())

    def test_edit_create_unconfirmed_parent_block_confirm_Contact_Address(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='user').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        contact_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_CONTACT(AHJID))
        contact_id = contact_response.json()['RecordID']
        address_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ADDRESS(contact_id, 'Contact'))
        edit_id = address_response.json()['EditID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)

        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        self.assertIsNone(Edit.objects.get(pk=edit_id).IsConfirmed)

    def test_edit_create_confirm_Address_Location(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        address_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ADDRESS(AHJID, 'AHJ'))
        address_id = address_response.json()['RecordID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='user').key)
        location_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_LOCATION(address_id))
        edit_id = location_response.json()['EditID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)

        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        self.assertTrue(Edit.objects.get(pk=edit_id).IsConfirmed)

    def test_edit_create_reject_Address_Location(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        address_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ADDRESS(AHJID, 'AHJ'))
        address_id = address_response.json()['RecordID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='user').key)
        location_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_LOCATION(address_id))
        location_id = location_response.json()['RecordID']
        edit_id = location_response.json()['EditID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)

        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'rejected'))

        self.assertFalse(Edit.objects.get(pk=edit_id).IsConfirmed)
        self.assertFalse(Location.objects.filter(id=location_id).exists())

    def test_edit_create_unconfirmed_parent_block_confirm_Address_Location(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='user').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        address_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ADDRESS(AHJID, 'AHJ'))
        address_id = address_response.json()['RecordID']
        location_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_LOCATION(address_id))
        edit_id = location_response.json()['EditID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)

        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'accepted'))

        self.assertIsNone(Edit.objects.get(pk=edit_id).IsConfirmed)

    def test_edit_create_AHJ_whole(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        ahj_address_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ADDRESS(AHJID, 'AHJ'))
        ahj_address_id = ahj_address_response.json()['RecordID']
        ahj_address_location_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_LOCATION(ahj_address_id))
        ahj_address_location_id = ahj_address_location_response.json()['RecordID']
        contact_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_CONTACT(AHJID))
        contact_id = contact_response.json()['RecordID']
        contact_address_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ADDRESS(contact_id, 'Contact'))
        contact_address_id = contact_address_response.json()['RecordID']
        contact_address_location_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_LOCATION(contact_address_id))
        contact_address_location_id = contact_address_location_response.json()['RecordID']
        eng_rev_req_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ENG_REV_REQ(AHJID))
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
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='user').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        edit_id = ahj_response.json()['EditID']
        ahj_address_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ADDRESS(AHJID, 'AHJ'))
        ahj_address_id = ahj_address_response.json()['RecordID']
        ahj_address_location_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_LOCATION(ahj_address_id))
        ahj_address_location_id = ahj_address_location_response.json()['RecordID']
        contact_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_CONTACT(AHJID))
        contact_id = contact_response.json()['RecordID']
        contact_address_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ADDRESS(contact_id, 'Contact'))
        contact_address_id = contact_address_response.json()['RecordID']
        contact_address_location_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_LOCATION(contact_address_id))
        contact_address_location_id = contact_address_location_response.json()['RecordID']
        eng_rev_req_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ENG_REV_REQ(AHJID))
        eng_rev_req_id = eng_rev_req_response.json()['RecordID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)

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

    """
    Test deleting records with Edit
    """

    def test_edit_delete_AHJ_alone(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)

        AHJID = ahj_response.json()['RecordID']

        delete_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(AHJID, 'AHJ'))

        self.assertTrue(delete_response.status_code == 200)
        self.assertFalse(AHJ.objects.filter(AHJID=AHJID).exists())

    def test_edit_delete_reject_AHJ_alone(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='user').key)
        delete_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(AHJID, 'AHJ'))
        edit_id = delete_response.json()['EditID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)

        self.client.get(EDIT_DETAIL_ENDPOINT_CONFIRM(edit_id, 'rejected'))

        self.assertFalse(Edit.objects.get(pk=edit_id).IsConfirmed)
        self.assertTrue(AHJ.objects.filter(AHJID=AHJID).exists())

    def test_edit_delete_unconfirmed_record_block_delete_AHJ_alone(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='user').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)

        delete_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(AHJID, 'AHJ'))

        self.assertTrue(delete_response.status_code == 200)
        self.assertTrue(AHJ.objects.filter(AHJID=AHJID).exists())

    def test_edit_delete_Address_from_AHJ(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        address_create_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ADDRESS(AHJID, 'AHJ'))
        address_id = address_create_response.json()['RecordID']

        delete_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(address_id, 'Address'))

        self.assertTrue(delete_response.status_code == 200)
        self.assertFalse(Address.objects.filter(AHJ=AHJ.objects.get(AHJID=AHJID)).exists())

    def test_edit_delete_unconfirmed_record_block_delete_Address_from_AHJ(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='user').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        address_create_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ADDRESS(AHJID, 'AHJ'))
        address_id = address_create_response.json()['RecordID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)

        delete_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(address_id, 'Address'))

        self.assertTrue(delete_response.status_code == 200)
        self.assertTrue(Address.objects.filter(AHJ=AHJ.objects.get(AHJID=AHJID)).exists())

    def test_edit_delete_Contact_from_AHJ(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        contact_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_CONTACT(AHJID))
        contact_id = contact_response.json()['RecordID']

        delete_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(contact_id, 'Contact'))

        self.assertTrue(delete_response.status_code == 200)
        self.assertFalse(Contact.objects.filter(AHJ=AHJ.objects.get(AHJID=AHJID)).exists())

    def test_edit_delete_unconfirmed_record_block_delete_Contact_from_AHJ(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='user').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        contact_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_CONTACT(AHJID))
        contact_id = contact_response.json()['RecordID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)

        delete_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(contact_id, 'Contact'))

        self.assertTrue(delete_response.status_code == 200)
        self.assertTrue(Contact.objects.filter(AHJ=AHJ.objects.get(AHJID=AHJID)).exists())

    def test_edit_delete_EngRevReq_from_AHJ(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        eng_rev_req_create_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ENG_REV_REQ(AHJID))
        eng_rev_req_id = eng_rev_req_create_response.json()['RecordID']

        delete_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(eng_rev_req_id, 'EngineeringReviewRequirement'))

        self.assertTrue(delete_response.status_code == 200)
        self.assertFalse(EngineeringReviewRequirement.objects.filter(AHJ=AHJ.objects.get(AHJID=AHJID)).exists())

    def test_edit_delete_unconfirmed_record_block_delete_EngRevReq_from_AHJ(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='user').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        eng_rev_req_create_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ENG_REV_REQ(AHJID))
        eng_rev_req_id = eng_rev_req_create_response.json()['RecordID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)

        delete_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(eng_rev_req_id, 'EngineeringReviewRequirement'))

        self.assertTrue(delete_response.status_code == 200)
        self.assertTrue(EngineeringReviewRequirement.objects.filter(AHJ=AHJ.objects.get(AHJID=AHJID)).exists())

    def test_edit_delete_Address_from_Contact(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        contact_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_CONTACT(AHJID))
        contact_id = contact_response.json()['RecordID']
        address_create_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ADDRESS(contact_id, 'Contact'))
        address_id = address_create_response.json()['RecordID']

        delete_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(address_id, 'Address'))

        self.assertTrue(delete_response.status_code == 200)
        self.assertFalse(Address.objects.filter(Contact=Contact.objects.get(id=contact_id)).exists())

    def test_edit_delete_unconfirmed_record_block_delete_Address_from_Contact(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='user').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        contact_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_CONTACT(AHJID))
        contact_id = contact_response.json()['RecordID']
        address_create_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ADDRESS(contact_id, 'Contact'))
        address_id = address_create_response.json()['RecordID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)

        delete_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(address_id, 'Address'))

        self.assertTrue(delete_response.status_code == 200)
        self.assertTrue(Address.objects.filter(Contact=Contact.objects.get(id=contact_id)).exists())

    def test_edit_delete_Location_from_Address(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        address_create_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ADDRESS(AHJID, 'AHJ'))
        address_id = address_create_response.json()['RecordID']
        location_create_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_LOCATION(address_id))
        location_id = location_create_response.json()['RecordID']

        delete_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(location_id, 'Location'))

        self.assertTrue(delete_response.status_code == 200)
        self.assertFalse(Location.objects.filter(Address=Address.objects.get(id=address_id)).exists())

    def test_edit_delete_unconfirmed_record_block_delete_Location_from_Address(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='user').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        address_create_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ADDRESS(AHJID, 'AHJ'))
        address_id = address_create_response.json()['RecordID']
        location_create_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_LOCATION(address_id))
        location_id = location_create_response.json()['RecordID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)

        delete_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(location_id, 'Location'))

        self.assertTrue(delete_response.status_code == 200)
        self.assertTrue(Location.objects.filter(Address=Address.objects.get(id=address_id)).exists())

    def test_edit_delete_AHJ_whole(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        ahj_address_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ADDRESS(AHJID, 'AHJ'))
        ahj_address_id = ahj_address_response.json()['RecordID']
        ahj_address_location_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_LOCATION(ahj_address_id))
        ahj_address_location_id = ahj_address_location_response.json()['RecordID']
        contact_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_CONTACT(AHJID))
        contact_id = contact_response.json()['RecordID']
        contact_address_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ADDRESS(contact_id, 'Contact'))
        contact_address_id = contact_address_response.json()['RecordID']
        contact_address_location_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_LOCATION(contact_address_id))
        contact_address_location_id = contact_address_location_response.json()['RecordID']
        eng_rev_req_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ENG_REV_REQ(AHJID))
        eng_rev_req_id = eng_rev_req_response.json()['RecordID']

        delete_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(AHJID, 'AHJ'))

        self.assertTrue(delete_response.status_code == 200)

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
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='user').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        ahj_address_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ADDRESS(AHJID, 'AHJ'))
        ahj_address_id = ahj_address_response.json()['RecordID']
        ahj_address_location_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_LOCATION(ahj_address_id))
        ahj_address_location_id = ahj_address_location_response.json()['RecordID']
        contact_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_CONTACT(AHJID))
        contact_id = contact_response.json()['RecordID']
        contact_address_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ADDRESS(contact_id, 'Contact'))
        contact_address_id = contact_address_response.json()['RecordID']
        contact_address_location_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_LOCATION(contact_address_id))
        contact_address_location_id = contact_address_location_response.json()['RecordID']
        eng_rev_req_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ENG_REV_REQ(AHJID))
        eng_rev_req_id = eng_rev_req_response.json()['RecordID']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)

        delete_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(AHJID, 'AHJ'))
        self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(ahj_address_id, 'Address'))
        self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(ahj_address_location_id, 'Location'))
        self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(contact_id, 'Contact'))
        self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(contact_address_id, 'Address'))
        self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(contact_address_location_id, 'Location'))
        self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_DELETE(eng_rev_req_id, 'EngineeringReviewRequirement'))

        self.assertTrue(delete_response.status_code == 200)

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
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        RecordID = ahj_response.json()['RecordID']
        RecordType = 'AHJ'
        FieldName = 'AHJName'
        Value = 'new_name'

        update_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(RecordID, RecordType, FieldName, Value))

        self.assertTrue(update_response.status_code == 200)
        self.assertTrue(getattr(AHJ.objects.get(AHJID=RecordID), FieldName) == Value)

    def test_edit_update_AHJ_TextField(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        RecordID = ahj_response.json()['RecordID']
        RecordType = 'AHJ'
        FieldName = 'Description'
        Value = 'new_description'

        update_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(RecordID, RecordType, FieldName, Value))

        self.assertTrue(update_response.status_code == 200)
        self.assertTrue(getattr(AHJ.objects.get(AHJID=RecordID), FieldName) == Value)

    def test_edit_update_AHJ_ChoiceField(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        RecordID = ahj_response.json()['RecordID']
        RecordType = 'AHJ'
        FieldName = 'BuildingCode'
        Value = '2021IBC'

        update_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(RecordID, RecordType, FieldName, Value))

        self.assertTrue(update_response.status_code == 200)
        self.assertTrue(getattr(AHJ.objects.get(AHJID=RecordID), FieldName) == Value)

    def test_edit_update_Location_DecimalField(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user__email_address='super').key)
        ahj_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_AHJ)
        AHJID = ahj_response.json()['RecordID']
        address_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_ADDRESS(AHJID, 'AHJ'))
        address_id = address_response.json()['RecordID']
        locaiton_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_CREATE_LOCATION(address_id))
        RecordID = locaiton_response.json()['RecordID']
        RecordType = 'Location'
        FieldName = 'Altitude'
        Value = 1000

        update_response = self.client.post(EDIT_SUBMIT_ENDPOINT, EDIT_UPDATE(RecordID, RecordType, FieldName, Value))
        print(update_response.json())
        self.assertTrue(update_response.status_code == 200)
        self.assertTrue(getattr(Location.objects.get(id=RecordID), FieldName) == Value)
