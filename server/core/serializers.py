from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from .models import *


class EditSerializerHelper(serializers.Field):

    def to_representation(self, value):
        if self.field_name[-2:].lower() == 'id':
            return EditSerializer(value.get_create_edit()).data
        return EditSerializer(value.get_edit(self.field_name)).data

    def to_internal_value(self, data):
        pass


class OrangeButtonDecimalFieldSerializer(serializers.DecimalField):

    def __init__(self, required, unit, decimal_or_precision, max_digits, decimal_places):
        super().__init__(max_digits=max_digits, decimal_places=decimal_places)
        self.required = required
        self.unit = unit
        self.decimal_or_precision = decimal_or_precision

    def to_representation(self, value):
        if self.decimal_or_precision == 'Decimal':
            return {'Decimal': self.decimal_places, 'Unit': self.unit, 'Value': value}
        elif self.decimal_or_precision == 'Precision':
            return {'Unit': self.unit, 'Value': value, 'Precision': self.max_digits}

    def to_internal_value(self, data):
        return data['Value']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'is_superuser',
            'email_address'
        ]


class EditSerializer(serializers.ModelSerializer):
    EditID = serializers.IntegerField(source='id', required=False)
    RecordID = serializers.CharField(required=False)
    ParentID = serializers.CharField(required=False)
    ParentRecordType = serializers.CharField(required=False)
    PreviousValue = serializers.CharField(required=False)
    FieldName = serializers.CharField(required=False)
    Value = serializers.CharField(required=False)
    IsConfirmed = serializers.NullBooleanField(required=False)
    ConfirmingUserID = UserSerializer(source='get_user_confirm', required=False)
    ModifyingUserID = UserSerializer(source='get_user_modify', required=False)
    ModifiedDate = serializers.DateTimeField(required=False)

    class Meta:
        model = Edit
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    LocationID = EditSerializerHelper(source='*', required=False)
    Altitude = OrangeButtonDecimalFieldSerializer(required=False, unit='Foot', decimal_or_precision='Decimal', max_digits=15, decimal_places=6)
    Description = EditSerializerHelper(source='*', required=False)
    Elevation = OrangeButtonDecimalFieldSerializer(required=False, unit='Foot', decimal_or_precision='Decimal', max_digits=15, decimal_places=6)
    Latitude = OrangeButtonDecimalFieldSerializer(required=False, unit='Degree', decimal_or_precision='Precision', max_digits=8, decimal_places=6)
    LocationDeterminationMethod = EditSerializerHelper(source='*', required=False)
    LocationType = EditSerializerHelper(source='*', required=False)
    Longitude = OrangeButtonDecimalFieldSerializer(required=False, unit='Degree', decimal_or_precision='Precision', max_digits=9, decimal_places=6)

    class Meta:
        model = Location
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    AddressID = EditSerializerHelper(source='*', required=False)
    AddrLine1 = EditSerializerHelper(source='*', required=False)
    AddrLine2 = EditSerializerHelper(source='*', required=False)
    AddrLine3 = EditSerializerHelper(source='*', required=False)
    AddressType = EditSerializerHelper(source='*', required=False)
    City = EditSerializerHelper(source='*', required=False)
    Country = EditSerializerHelper(source='*', required=False)
    County = EditSerializerHelper(source='*', required=False)
    Description = EditSerializerHelper(source='*', required=False)
    StateProvince = EditSerializerHelper(source='*', required=False)
    ZipPostalCode = EditSerializerHelper(source='*', required=False)
    Location = LocationSerializer(source='location', many=False, required=False, allow_null=True)

    class Meta:
        model = Address
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    ContactID = EditSerializerHelper(source='*', required=False)
    ContactType = EditSerializerHelper(source='*', required=False)
    Description = EditSerializerHelper(source='*', required=False)
    Email = EditSerializerHelper(source='*', required=False)
    FirstName = EditSerializerHelper(source='*', required=False)
    HomePhone = EditSerializerHelper(source='*', required=False)
    LastName = EditSerializerHelper(source='*', required=False)
    MiddleName = EditSerializerHelper(source='*', required=False)
    MobilePhone = EditSerializerHelper(source='*', required=False)
    WorkPhone = EditSerializerHelper(source='*', required=False)
    Address = AddressSerializer(source='address', many=False, required=False, allow_null=True)

    class Meta:
        model = Contact
        fields = '__all__'


class EngineeringReviewRequirementSerializer(serializers.ModelSerializer):
    EngineeringReviewRequirementID = EditSerializerHelper(source='*', required=False)
    RequirementLevel = EditSerializerHelper(source='*', required=False)
    StampType = EditSerializerHelper(source='*', required=False)
    Description = EditSerializerHelper(source='*', required=False)
    EngineeringReviewType = EditSerializerHelper(source='*', required=False)

    class Meta:
        model = EngineeringReviewRequirement
        fields = '__all__'


class AHJSerializer(serializers.ModelSerializer):
    AHJID = EditSerializerHelper(source='*', required=False)
    AHJName = EditSerializerHelper(source='*', required=False)
    BuildingCode = EditSerializerHelper(source='*', required=False)
    BuildingCodeNotes = EditSerializerHelper(source='*', required=False)
    Description = EditSerializerHelper(source='*', required=False)
    DocumentSubmissionMethod = EditSerializerHelper(source='*', required=False)
    DocumentSubmissionMethodNotes = EditSerializerHelper(source='*', required=False)
    ElectricCode = EditSerializerHelper(source='*', required=False)
    ElectricCodeNotes = EditSerializerHelper(source='*', required=False)
    FileFolderURL = EditSerializerHelper(source='*', required=False)
    FireCode = EditSerializerHelper(source='*', required=False)
    FireCodeNotes = EditSerializerHelper(source='*', required=False)
    ResidentialCode = EditSerializerHelper(source='*', required=False)
    ResidentialCodeNotes = EditSerializerHelper(source='*', required=False)
    WindCode = EditSerializerHelper(source='*', required=False)
    WindCodeNotes = EditSerializerHelper(source='*', required=False)
    Address = AddressSerializer(source='address', many=False, required=False, allow_null=True)
    Contacts = ContactSerializer(source='contact_set', many=True, required=False)
    EngineeringReviewRequirements = EngineeringReviewRequirementSerializer(source='engineeringreviewrequirement_set', many=True, required=False)
    confirmed_edits_only = False

    class Meta:
        model = AHJ
        fields = '__all__'


class LocationHistorySerializer(serializers.ModelSerializer):
    history_user = UserSerializer(many=False)

    class Meta:
        model = Location.history.model
        fields = '__all__'


class AddressHistorySerializer(serializers.ModelSerializer):
    history_user = UserSerializer(many=False)

    class Meta:
        model = Address.history.model
        fields = '__all__'


class ContactHistorySerializer(serializers.ModelSerializer):
    history_user = UserSerializer(many=False)

    class Meta:
        model = Contact.history.model
        fields = '__all__'


class EngineeringReviewRequirementHistorySerializer(serializers.ModelSerializer):
    history_user = UserSerializer(many=False)

    class Meta:
        model = EngineeringReviewRequirement.history.model
        fields = '__all__'


class AHJHistorySerializer(serializers.ModelSerializer):
    history_user = UserSerializer(many=False)

    class Meta:
        model = AHJ.history.model
        fields = '__all__'
