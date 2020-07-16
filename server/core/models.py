from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError
from ahj_gis.models import Polygon
from django.apps import apps
import json
from taggit.managers import TaggableManager
from simple_history.models import HistoricalRecords
from django.utils import timezone

import uuid
# Authentication and Authorization

BUILDING_CODE_CHOICES = [
    ('2021IBC', '2021 IBC'),
    ('2018IBC', '2018 IBC'),
    ('2015IBC', '2015 IBC'),
    ('2012IBC', '2012 IBC'),
    ('2009IBC', '2009 IBC'),
    ('NoSolarRegulations', 'No Solar Regulations')
]

ELECTRIC_CODE_CHOICES = [
    ('2020NEC', '2020 NEC'),
    ('2017NEC', '2017 NEC'),
    ('2014NEC', '2014 NEC'),
    ('2011NEC', '2011 NEC'),
    ('NoSolarRegulations', 'No Solar Regulations')
]

FIRE_CODE_CHOICES = [
    ('2021IFC', '2021 IFC'),
    ('2018IFC', '2018 IFC'),
    ('2015IFC', '2015 IFC'),
    ('2012IFC', '2012 IFC'),
    ('2009IFC', '2009 IFC'),
    ('NoSolarRegulations', 'No Solar Regulations')
]

RESIDENTIAL_CODE_CHOICES = [
    ('2021IRC', '2021 IRC'),
    ('2018IRC', '2018 IRC'),
    ('2015IRC', '2015 IRC'),
    ('2012IRC', '2012 IRC'),
    ('2009IRC', '2009 IRC'),
    ('NoSolarRegulations', 'No Solar Regulations')
]

WIND_CODE_CHOICES = [
    ('ASCE716', 'ASCE7-16'),
    ('ASCE710', 'ASCE7-10'),
    ('ASCE705', 'ASCE7-05'),
    ('SpecialWindZone', 'Special Wind Zone')
]

DOCUMENT_SUBMISSION_METHOD_CHOICES = [
    ('Epermitting', 'Epermitting'),
    ('Email', 'Email'),
    ('InPerson', 'In Person'),
    ('SolarApp', 'SolarAPP')
]

ADDRESS_TYPE_CHOICES = [
    ('Mailing', 'Mailing'),
    ('Billing', 'Billing'),
    ('Installation', 'Installation'),
    ('Shipping', 'Shipping')
]

LOCATION_DETERMINATION_METHOD_CHOICES = [
    ('GPS', 'GPS'),
    ('Survey', 'Survey'),
    ('AerialImage', 'Aerial Image'),
    ('EngineeringReport', 'Engineering Report'),
    ('AddressGeocoding', 'Address Geocoding'),
    ('Unknown', 'Unknown')
]

LOCATION_TYPE_CHOICES = [
    ('DeviceSpecific', 'Device Specific'),
    ('SiteEntrance', 'Site Entrance'),
    ('GeneralProximity', 'General Proximity'),
    ('Warehouse', 'Warehouse')
]

CONTACT_TYPE_CHOICES = [
    ('Homeowner', 'Homeowner'),
    ('OffTaker', 'Off Taker'),
    ('Inspector', 'Inspector'),
    ('Engineer', 'Engineer'),
    ('Originator', 'Originator'),
    ('Installer', 'Installer'),
    ('Investor', 'Investor'),
    ('PermittingOfficial', 'Permitting Official'),
    ('FireMarshal', 'Fire Marshal'),
    ('ProjectManager', 'Project Manager')
]

PREFERRED_CONTACT_METHOD_CHOICES = [
    ('Email', 'Email'),
    ('WorkPhone', 'Work Phone'),
    ('CellPhone', 'Cell Phone'),
    ('HomePhone', 'Home Phone'),
    ('CellTextMessage', 'Cell Text Message'),
]

ENGINEERING_REVIEW_TYPE_CHOICES = [
    ('StructuralEngineer', 'Structural Engineer'),
    ('ElectricalEngineer', 'Electrical Engineer'),
    ('PVEngineer', 'PV Engineer'),
    ('MasterElectrician', 'Master Electrician'),
    ('FireMarshal', 'Fire Marshal'),
    ('EnvironmentalEngineer', 'Environmental Engineer')
]

REQUIREMENT_LEVEL_CHOICES = [
    ('Required', 'Required'),
    ('Optional', 'Optional'),
    ('ConditionallyRequired', 'Conditionally Required')
]

STAMP_TYPE_CHOICES = [
    ('Wet', 'Wet'),
    ('Digital', 'Digital'),
    ('Notary', 'Notary'),
    ('None', 'None')
]


def retrieve_edit(record, field_name, edit):
    if edit is None:
        return Edit(Value=getattr(record, field_name), FieldName=field_name)
    else:
        return edit

    
def get_edit(record, field_name, find_create_edit, confirmed_edits_only, highest_vote_ranking):
    if record.__class__.__name__ == 'AHJ':
        record_edits = Edit.objects.filter(RecordID=record.AHJID)
    else:
        record_edits = Edit.objects.filter(RecordID=record.id).filter(RecordType=record.__class__.__name__)

    if find_create_edit:
        edit = record_edits.filter(EditType='create').first()
        return retrieve_edit(record, field_name, edit)

    record_edits_field_name = record_edits.filter(FieldName=field_name)
    if confirmed_edits_only:
        edit = record_edits_field_name.filter(IsConfirmed=True).order_by('-ConfirmedDate').first()
        return retrieve_edit(record, field_name, edit)
    elif highest_vote_ranking:
        edit = record_edits_field_name.order_by('-VoteRanking').first()
        return retrieve_edit(record, field_name, edit)
    else:
        edit = record_edits_field_name.order_by('-ModifiedDate').first()
        return retrieve_edit(record, field_name, edit)


def add_delete_edits(record, edit):
    # The record will never be an AHJ record
    Edit.objects.create(RecordID=record.id, RecordType=record.__class__.__name__, EditType='delete',
                        ModifyingUserID=edit.ModifyingUserID,
                        ModifiedDate=edit.ModifiedDate, IsConfirmed=True, ConfirmingUserID=edit.ConfirmingUserID,
                        ConfirmedDate=edit.ConfirmedDate)
        

# Create an auth token every time a user is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email_address, password, **extra_fields):
        if not email_address:
            raise ValueError('The given email_address must be set')
        email_address = self.normalize_email(email_address)
        user = self.model(email_address=email_address, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email_address, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email_address, password, **extra_fields)

    def create_superuser(self, email_address, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email_address, password, **extra_fields)


class User(AbstractBaseUser):
    identifier = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    email_address = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    # FK one to many
    # entity = models.ForeignKey(Entity, on_delete=models.CASCADE, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email_address'
    EMAIL_FIELD = 'email_address'

    def __str__(self):
        return self.email_address

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, core):
        return self.is_superuser

    @property
    def is_staff(self):
        return self.is_superuser

    tags = TaggableManager()


class AHJ(models.Model):
    mpoly = models.ForeignKey(Polygon, null=True, on_delete=models.DO_NOTHING)
    AHJID = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    AHJName = models.CharField(blank=True, max_length=100)
    BuildingCode = models.CharField(choices=BUILDING_CODE_CHOICES, blank=True, default='', max_length=45)
    BuildingCodeNotes = models.CharField(blank=True, max_length=255)
    Description = models.TextField(blank=True)
    DocumentSubmissionMethod = models.CharField(choices=DOCUMENT_SUBMISSION_METHOD_CHOICES, blank=True, default='', max_length=45)
    DocumentSubmissionMethodNotes = models.CharField(blank=True, max_length=255)
    ElectricCode = models.CharField(choices=ELECTRIC_CODE_CHOICES, blank=True, default='', max_length=45)
    ElectricCodeNotes = models.CharField(blank=True, max_length=255)
    FileFolderURL = models.CharField(blank=True, max_length=255)
    FireCode = models.CharField(choices=FIRE_CODE_CHOICES, blank=True, default='', max_length=45)
    FireCodeNotes = models.CharField(blank=True, max_length=255)
    ResidentialCode = models.CharField(choices=RESIDENTIAL_CODE_CHOICES, blank=True, default='', max_length=45)
    ResidentialCodeNotes = models.CharField(blank=True, max_length=255)
    WindCode = models.CharField(choices=WIND_CODE_CHOICES, blank=True, default='', max_length=45)
    WindCodeNotes = models.CharField(blank=True, max_length=255)
    history = HistoricalRecords()

    confirmed_edits_only = False
    highest_vote_ranking = False

    edit_set = None

    def get_edit(self, field_name):
        return get_edit(record=self, field_name=field_name, find_create_edit=False, confirmed_edits_only=self.confirmed_edits_only, highest_vote_ranking=self.highest_vote_ranking)

    def get_create_edit(self):
        return get_edit(record=self, field_name='AHJID', find_create_edit=True,  confirmed_edits_only=self.confirmed_edits_only, highest_vote_ranking=self.highest_vote_ranking)

    def chain_delete(self, edit):
        address = Address.objects.filter(AHJ=self).first()
        if address is not None:
            address.chain_delete(edit)
        contacts = Contact.objects.filter(AHJ=self)
        for contact in contacts:
            contact.chain_delete(edit)
        eng_rev_reqs = EngineeringReviewRequirement.objects.filter(AHJ=self)
        for eng_rev_req in eng_rev_reqs:
            eng_rev_req.chain_delete(edit)
        self.delete()


class Contact(models.Model):
    AHJ = models.ForeignKey(AHJ, to_field='AHJID', null=True, on_delete=models.CASCADE)
    ContactTimezone = models.CharField(blank=True, max_length=100)
    ContactType = models.CharField(choices=CONTACT_TYPE_CHOICES, blank=True, default='', max_length=45)
    Description = models.TextField(blank=True)
    Email = models.CharField(blank=True, max_length=100)
    FirstName = models.CharField(blank=True, max_length=100)
    HomePhone = models.CharField(blank=True, max_length=31)
    LastName = models.CharField(blank=True, max_length=100)
    MiddleName = models.CharField(blank=True, max_length=100)
    MobilePhone = models.CharField(blank=True, max_length=31)
    PreferredContactMethod = models.CharField(choices=PREFERRED_CONTACT_METHOD_CHOICES, blank=True, default='', max_length=45)
    Title = models.CharField(blank=True, max_length=100)
    WorkPhone = models.CharField(blank=True, max_length=31)
    history = HistoricalRecords()

    confirmed_edits_only = False
    highest_vote_ranking = False

    def get_edit(self, field_name):
        return get_edit(record=self, field_name=field_name, find_create_edit=False, confirmed_edits_only=self.confirmed_edits_only, highest_vote_ranking=self.highest_vote_ranking)

    def get_create_edit(self):
        return get_edit(record=self, field_name='id', find_create_edit=True,  confirmed_edits_only=self.confirmed_edits_only, highest_vote_ranking=self.highest_vote_ranking)

    def chain_delete(self, edit):
        address = Address.objects.filter(Contact=self).first()
        if address is not None:
            address.chain_delete(edit)
        add_delete_edits(self, edit)
        self.delete()


class EngineeringReviewRequirement(models.Model):
    AHJ = models.ForeignKey(AHJ, to_field='AHJID', null=True, on_delete=models.CASCADE)
    Description = models.TextField(blank=True)
    EngineeringReviewType = models.CharField(choices=ENGINEERING_REVIEW_TYPE_CHOICES, blank=True, default='', max_length=45)
    RequirementLevel = models.CharField(choices=REQUIREMENT_LEVEL_CHOICES, blank=True, default='', max_length=45)
    StampType = models.CharField(choices=STAMP_TYPE_CHOICES, max_length=45)
    history = HistoricalRecords()

    confirmed_edits_only = False
    highest_vote_ranking = False

    def get_edit(self, field_name):
        return get_edit(record=self, field_name=field_name, find_create_edit=False, confirmed_edits_only=self.confirmed_edits_only, highest_vote_ranking=self.highest_vote_ranking)

    def get_create_edit(self):
        return get_edit(record=self, field_name='id', find_create_edit=True,  confirmed_edits_only=self.confirmed_edits_only, highest_vote_ranking=self.highest_vote_ranking)

    def chain_delete(self, edit):
        add_delete_edits(self, edit)
        self.delete()


class Address(models.Model):
    AHJ = models.OneToOneField(AHJ, to_field='AHJID', null=True, blank=True, on_delete=models.CASCADE)
    Contact = models.OneToOneField(Contact, null=True, blank=True, on_delete=models.CASCADE)
    AddrLine1 = models.CharField(blank=True, max_length=100)
    AddrLine2 = models.CharField(blank=True, max_length=100)
    AddrLine3 = models.CharField(blank=True, max_length=100)
    AddressType = models.CharField(choices=ADDRESS_TYPE_CHOICES, blank=True, default='', max_length=45)
    City = models.CharField(blank=True, max_length=100)
    Country = models.CharField(blank=True, max_length=100)
    County = models.CharField(blank=True, max_length=100)
    Description = models.TextField(blank=True)
    StateProvince = models.CharField(blank=True, max_length=100)
    ZipPostalCode = models.CharField(blank=True, max_length=10)
    history = HistoricalRecords()

    confirmed_edits_only = False
    highest_vote_ranking = False

    def get_edit(self, field_name):
        return get_edit(record=self, field_name=field_name, find_create_edit=False, confirmed_edits_only=self.confirmed_edits_only, highest_vote_ranking=self.highest_vote_ranking)

    def get_create_edit(self):
        return get_edit(record=self, field_name='id', find_create_edit=True,  confirmed_edits_only=self.confirmed_edits_only, highest_vote_ranking=self.highest_vote_ranking)

    def chain_delete(self, edit):
        location = Location.objects.filter(Address=self).first()
        if location is not None:
            location.chain_delete(edit)
        add_delete_edits(self, edit)
        self.delete()


class Location(models.Model):
    Address = models.OneToOneField(Address, on_delete=models.CASCADE)
    Altitude = models.DecimalField(null=True, max_digits=15, decimal_places=6)
    Description = models.TextField(blank=True)
    Elevation = models.DecimalField(null=True, max_digits=15, decimal_places=6)
    Latitude = models.DecimalField(null=True, max_digits=8, decimal_places=6)
    LocationDeterminationMethod = models.CharField(choices=LOCATION_DETERMINATION_METHOD_CHOICES, blank=True, default='', max_length=45)
    LocationType = models.CharField(choices=LOCATION_TYPE_CHOICES, blank=True, default='', max_length=45)
    Longitude = models.DecimalField(null=True, max_digits=9, decimal_places=6)
    history = HistoricalRecords()

    confirmed_edits_only = False
    highest_vote_ranking = False

    def get_edit(self, field_name):
        return get_edit(record=self, field_name=field_name, find_create_edit=False, confirmed_edits_only=self.confirmed_edits_only, highest_vote_ranking=self.highest_vote_ranking)

    def get_create_edit(self):
        return get_edit(record=self, field_name='id', find_create_edit=True,  confirmed_edits_only=self.confirmed_edits_only, highest_vote_ranking=self.highest_vote_ranking)

    def chain_delete(self, edit):
        add_delete_edits(self, edit)
        self.delete()


class Edit(models.Model):
    RecordID = models.CharField(max_length=45)
    RecordType = models.CharField(max_length=45)
    ParentID = models.CharField(default='', max_length=45)
    ParentRecordType = models.CharField(default='', max_length=45)
    EditType = models.CharField(max_length=45)
    FieldName = models.CharField(default='', max_length=45)
    Value = models.TextField(default='')
    PreviousValue = models.TextField(default='')
    ModifyingUserID = models.IntegerField()
    ModifiedDate = models.DateTimeField(auto_now_add=True)
    IsConfirmed = models.BooleanField(null=True, default=None)
    ConfirmingUserID = models.IntegerField(null=True, default=None)
    ConfirmedDate = models.DateTimeField(null=True, default=None)
    VoteRating = models.IntegerField(default=0)

    def get_record_owner_id(self):
        return self.RecordID # wrong for now, add user ownership next

    def create_record(self):
        if self.RecordType == 'AHJ':
            record = apps.get_model('core', self.RecordType).objects.create()
            self.RecordID = record.AHJID
        else:
            record = apps.get_model('core', self.RecordType).objects.create(**{self.ParentRecordType: self.get_parent()})
            self.RecordID = record.id
        self.save()

    def get_parent(self):
        if self.ParentRecordType == 'AHJ':
            return apps.get_model('core', self.ParentRecordType).objects.filter(AHJID=self.ParentID).first()
        return apps.get_model('core', self.ParentRecordType).objects.filter(id=self.ParentID).first()

    def get_record(self):
        if self.RecordType == 'AHJ':
            record = AHJ.objects.filter(AHJID=self.RecordID).first()
        else:
            record = apps.get_model('core', self.RecordType).objects.filter(id=self.RecordID).first()
        return record

    def get_user_confirm(self):
        return User.objects.filter(pk=self.ConfirmingUserID).first()

    def get_user_modify(self):
        return User.objects.filter(pk=self.ModifyingUserID).first()

    def check_record_edit_create_confirmed(self, record):
        if record.__class__.__name__ == 'AHJ':
            create_edit = Edit.objects.filter(RecordID=record.AHJID).filter(RecordType=record.__class__.__name__).filter(EditType='create').first()
        else:
            create_edit = Edit.objects.filter(RecordID=record.id).filter(RecordType=record.__class__.__name__).filter(EditType='create').first()
        if create_edit is not None and create_edit.IsConfirmed:
            return True
        return False

    def accept(self, user_id):

        if self.EditType == 'create':
            if self.RecordType != 'AHJ':
                parent = self.get_parent()
                if not self.check_record_edit_create_confirmed(parent):
                    return
        elif self.EditType == 'update':
            record = self.get_record()
            if record is not None:
                if self.check_record_edit_create_confirmed(record):
                    setattr(record, self.FieldName, self.Value)
                    record.save()
        elif self.EditType == 'delete':
            self.get_record().chain_delete(self)

        self.IsConfirmed = True
        self.ConfirmingUserID = user_id
        self.ConfirmedDate = timezone.now()
        self.save()

    def reject(self, user_id):
        self.IsConfirmed = False
        self.ConfirmingUserID = user_id
        self.ConfirmedDate = timezone.now()

        if self.EditType == 'create':
            self.get_record().chain_delete(self)

        self.save()

    def validate_RecordType(self):
        try:
            apps.get_model('core', self.RecordType)
            return True
        except LookupError:
            return False

    def validate_ParentRecordType(self):
        try:
            apps.get_model('core', self.RecordType)
            return True
        except LookupError:
            return False

    def validate_FieldName(self):
        record = self.get_record()
        return hasattr(record, self.FieldName)
