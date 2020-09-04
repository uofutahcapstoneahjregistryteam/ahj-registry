from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from .models import *


class EditSerializerHelper(serializers.Field):
    def to_representation(self, value):
        if value.__class__.__name__ == self.field_name[0:-2] and self.field_name[-2:].lower() == 'id':
            return EditSerializer(value.get_create_edit(self.parent.context['confirmed_edits_only'], self.parent.context['highest_vote_rating'])).data
        return EditSerializer(value.get_edit(self.field_name, self.parent.context['confirmed_edits_only'], self.parent.context['highest_vote_rating'])).data

    def to_internal_value(self, data):
        pass


class UserSerializer(serializers.Serializer):
    UserID = serializers.IntegerField(source='id', required=False, read_only=True)
    Email = serializers.CharField(source='email_address')
    Password = serializers.CharField(source='password', write_only=True)
    FirstName = serializers.CharField(source='first_name')
    LastName = serializers.CharField(source='last_name')
    AHJ = serializers.UUIDField(source='AHJ__AHJID', read_only=True)

    def create(self, validated_data):
        Email = validated_data.get('email_address', '')
        Password = validated_data.get('password', '')
        FirstName = validated_data.get('first_name', '')
        LastName = validated_data.get('last_name', '')
        user = User.objects.create_user(email_address=Email, password=Password, first_name=FirstName, last_name=LastName, is_active=False)
        send_user_confirmation_email(user)
        return user

    def update(self, instance, validated_data):
        pass


class EditSerializer(serializers.Serializer):
    EditID = serializers.IntegerField(source='id', required=False, read_only=True)
    RecordID = serializers.CharField(required=False)
    RecordType = serializers.CharField(required=False)
    EditType = serializers.CharField(required=False)
    ParentID = serializers.CharField(required=False)
    ParentRecordType = serializers.CharField(required=False)
    PreviousValue = serializers.CharField(required=False, read_only=True)
    FieldName = serializers.CharField(required=False)
    Value = serializers.CharField(required=False, allow_blank=True)
    IsConfirmed = serializers.NullBooleanField(required=False, read_only=True)
    ConfirmingUserID = UserSerializer(source='get_user_confirm', required=False, read_only=True)
    ModifyingUserID = UserSerializer(source='get_user_modify', required=False, read_only=True)
    ModifiedDate = serializers.DateTimeField(required=False, read_only=True)
    VoteRating = serializers.IntegerField(required=False, read_only=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class LocationSerializer(serializers.Serializer):
    LocationID = EditSerializerHelper(source='*', required=False)
    Altitude = EditSerializerHelper(source='*', required=False)
    Description = EditSerializerHelper(source='*', required=False)
    Elevation = EditSerializerHelper(source='*', required=False)
    Latitude = EditSerializerHelper(source='*', required=False)
    LocationDeterminationMethod = EditSerializerHelper(source='*', required=False)
    LocationType = EditSerializerHelper(source='*', required=False)
    Longitude = EditSerializerHelper(source='*', required=False)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class AddressSerializer(serializers.Serializer):
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

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ContactSerializer(serializers.Serializer):
    ContactID = EditSerializerHelper(source='*', required=False)
    ContactType = EditSerializerHelper(source='*', required=False)
    ContactTimezone = EditSerializerHelper(source='*', required=False)
    Description = EditSerializerHelper(source='*', required=False)
    Email = EditSerializerHelper(source='*', required=False)
    FirstName = EditSerializerHelper(source='*', required=False)
    HomePhone = EditSerializerHelper(source='*', required=False)
    LastName = EditSerializerHelper(source='*', required=False)
    MiddleName = EditSerializerHelper(source='*', required=False)
    MobilePhone = EditSerializerHelper(source='*', required=False)
    WorkPhone = EditSerializerHelper(source='*', required=False)
    Title = EditSerializerHelper(source='*', required=False)
    PreferredContactMethod = EditSerializerHelper(source='*', required=False)
    URL = EditSerializerHelper(source='*', required=False)
    Address = AddressSerializer(source='address', many=False, required=False, allow_null=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class EngineeringReviewRequirementSerializer(serializers.Serializer):
    EngineeringReviewRequirementID = EditSerializerHelper(source='*', required=False)
    RequirementLevel = EditSerializerHelper(source='*', required=False)
    RequirementLevelNotes = EditSerializerHelper(source='*', required=False)
    StampType = EditSerializerHelper(source='*', required=False)
    Description = EditSerializerHelper(source='*', required=False)
    EngineeringReviewType = EditSerializerHelper(source='*', required=False)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class AHJSerializer(serializers.Serializer):
    AHJID = EditSerializerHelper(source='*', required=False)
    AHJCode = EditSerializerHelper(source='*', required=False)
    AHJName = EditSerializerHelper(source='*', required=False)
    AHJLevelCode = EditSerializerHelper(source='*', required=False)
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
    URL = EditSerializerHelper(source='*', required=False)
    WindCode = EditSerializerHelper(source='*', required=False)
    WindCodeNotes = EditSerializerHelper(source='*', required=False)
    Address = AddressSerializer(source='address', many=False, required=False, allow_null=True)
    Contacts = ContactSerializer(source='contact_set', many=True, required=False)
    EngineeringReviewRequirements = EngineeringReviewRequirementSerializer(source='engineeringreviewrequirement_set', many=True, required=False)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


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
