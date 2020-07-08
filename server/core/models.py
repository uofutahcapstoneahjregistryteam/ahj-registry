from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError
from ahj_gis.models import Polygon

from taggit.managers import TaggableManager
from simple_history.models import HistoricalRecords

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
    ('ASCE716', 'ASCE7-16'),
    ('ASCE716', 'ASCE7-16'),
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

    def __str__(self):
        return self.AHJName + ', ' + Address.objects.get(AHJ=self).StateProvince


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


class EngineeringReviewRequirement(models.Model):
    AHJ = models.ForeignKey(AHJ, to_field='AHJID', null=True, on_delete=models.CASCADE)
    Description = models.TextField(blank=True)
    EngineeringReviewType = models.CharField(choices=ENGINEERING_REVIEW_TYPE_CHOICES, blank=True, default='', max_length=45)
    RequirementLevel = models.CharField(choices=REQUIREMENT_LEVEL_CHOICES, blank=True, default='', max_length=45)
    StampType = models.CharField(choices=STAMP_TYPE_CHOICES, max_length=45)
    history = HistoricalRecords()


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


class Location(models.Model):
    Address = models.OneToOneField(Address, on_delete=models.CASCADE, primary_key=True)
    Altitude = models.DecimalField(null=True, max_digits=15, decimal_places=6)
    Description = models.TextField(blank=True)
    Elevation = models.DecimalField(null=True, max_digits=15, decimal_places=6)
    Latitude = models.DecimalField(null=True, max_digits=8, decimal_places=6)
    LocationDeterminationMethod = models.CharField(choices=LOCATION_DETERMINATION_METHOD_CHOICES, blank=True, default='', max_length=45)
    LocationType = models.CharField(choices=LOCATION_TYPE_CHOICES, blank=True, default='', max_length=45)
    Longitude = models.DecimalField(null=True, max_digits=9, decimal_places=6)
    history = HistoricalRecords()
