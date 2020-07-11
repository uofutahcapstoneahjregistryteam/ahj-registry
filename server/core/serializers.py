from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from .models import *


class OrangeButtonUUIDFieldSerializer(serializers.UUIDField):

    def to_representation(self, value):
        return {'Value': value}

    def to_internal_value(self, data):
        return data['Value']


class OrangeButtonCharFieldSerializer(serializers.CharField):

    def to_representation(self, value):
        return {'Value': value}

    def to_internal_value(self, data):
        return data['Value']


class OrangeButtonIntegerFieldSerializer(serializers.IntegerField):

    def to_representation(self, value):
        return {'Value': value}

    def to_internal_value(self, data):
        return data['Value']


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


class LocationSerializer(serializers.Serializer):
    LocationID = OrangeButtonIntegerFieldSerializer(source='Address_id', required=False)
    Altitude = OrangeButtonDecimalFieldSerializer(required=False, unit='Foot', decimal_or_precision='Decimal', max_digits=15, decimal_places=6)
    Description = OrangeButtonCharFieldSerializer(required=False)
    Elevation = OrangeButtonDecimalFieldSerializer(required=False, unit='Foot', decimal_or_precision='Decimal', max_digits=15, decimal_places=6)
    Latitude = OrangeButtonDecimalFieldSerializer(required=False, unit='Degree', decimal_or_precision='Precision', max_digits=8, decimal_places=6)
    LocationDeterminationMethod = OrangeButtonCharFieldSerializer(required=False)
    LocationType = OrangeButtonCharFieldSerializer(required=False)
    Longitude = OrangeButtonDecimalFieldSerializer(required=False, unit='Degree', decimal_or_precision='Precision', max_digits=9, decimal_places=6)

    def create(self, address, validated_data, edit):
        if validated_data.get('Address_id') is not None:
            validated_data.pop('Address_id')
        location = Location.objects.create(Address=address, **validated_data)
        add_create_edits(location, edit)
        return location

    def update(self, instance, validated_data):
        instance.Altitude = validated_data.get('Altitude', instance.Altitude)
        instance.Description = validated_data.get('Description', instance.Description)
        instance.Elevation = validated_data.get('Elevation', instance.Elevation)
        instance.Latitude = validated_data.get('Latitude', instance.Latitude)
        instance.LocationDeterminationMethod = validated_data.get('LocationDeterminationMethod', instance.LocationDeterminationMethod)
        instance.LocationType = validated_data.get('LocationType', instance.LocationType)
        instance.Longitude = validated_data.get('Longitude', instance.Longitude)
        instance.save()
        return instance

    def __delete__(self, instance, edit):
        add_delete_edits(instance, edit)
        instance.delete()


class AddressSerializer(serializers.Serializer):
    AddressID = OrangeButtonCharFieldSerializer(source='id', required=False)
    AddrLine1 = OrangeButtonCharFieldSerializer(required=False)
    AddrLine2 = OrangeButtonCharFieldSerializer(required=False)
    AddrLine3 = OrangeButtonCharFieldSerializer(required=False)
    AddressType = OrangeButtonCharFieldSerializer(required=False)
    City = OrangeButtonCharFieldSerializer(required=False)
    Country = OrangeButtonCharFieldSerializer(required=False)
    County = OrangeButtonCharFieldSerializer(required=False)
    Description = OrangeButtonCharFieldSerializer(required=False)
    StateProvince = OrangeButtonCharFieldSerializer(required=False)
    ZipPostalCode = OrangeButtonCharFieldSerializer(required=False)
    Location = LocationSerializer(source='location', many=False, required=False, allow_null=True)

    def create(self, model_object, model_object_type, validated_data, edit):
        # Do not specify an id for a new address
        if validated_data.get('id') is not None:
            validated_data.pop('id')

        # Pop off location object if it exists (done before creating address)
        location_data = None
        if validated_data.get('location') is not None:
            location_data = validated_data.pop('location')

        address = None
        if model_object_type == 'AHJ':
            address = Address.objects.create(AHJ=model_object, **validated_data)
        elif model_object_type == 'Contact':
            address = Address.objects.create(Contact=model_object, **validated_data)
        add_create_edits(address, edit)
        # If location object did exist, deserialize it
        if location_data is not None:
            LocationSerializer().create(address, location_data, edit)
        return address

    def update(self, instance, validated_data):
        instance.AddrLine1 = validated_data.get('AddrLine1', instance.AddrLine1)
        instance.AddrLine2 = validated_data.get('AddrLine2', instance.AddrLine2)
        instance.AddrLine3 = validated_data.get('AddrLine3', instance.AddrLine3)
        instance.AddressType = validated_data.get('AddressType', instance.AddressType)
        instance.City = validated_data.get('City', instance.City)
        instance.Country = validated_data.get('Country', instance.Country)
        instance.County = validated_data.get('County', instance.County)
        instance.Description = validated_data.get('Description', instance.Description)
        instance.StateProvince = validated_data.get('StateProvince', instance.StateProvince)
        instance.ZipPostalCode = validated_data.get('ZipPostalCode', instance.ZipPostalCode)
        instance.save()

        if validated_data.get('location') is not None:
            location_data = validated_data.pop('location')
            address_location = Location.objects.filter(Address=instance).first()
            if address_location is None:
                LocationSerializer().create(instance, location_data)
            else:
                LocationSerializer().update(address_location, location_data)

        return instance

    def __delete__(self, instance, edit):
        add_delete_edits(instance, edit)
        address_location = Location.objects.filter(Address=instance).first()
        if address_location is not None:
            LocationSerializer().__delete__(address_location, edit)
        instance.delete()


class ContactSerializer(serializers.Serializer):
    ContactID = OrangeButtonIntegerFieldSerializer(source='id', required=False)
    ContactType = OrangeButtonCharFieldSerializer(required=False)
    Description = OrangeButtonCharFieldSerializer(required=False)
    Email = OrangeButtonCharFieldSerializer(required=False)
    FirstName = OrangeButtonCharFieldSerializer(required=False)
    HomePhone = OrangeButtonCharFieldSerializer(required=False)
    LastName = OrangeButtonCharFieldSerializer(required=False)
    MiddleName = OrangeButtonCharFieldSerializer(required=False)
    MobilePhone = OrangeButtonCharFieldSerializer(required=False)
    WorkPhone = OrangeButtonCharFieldSerializer(required=False)
    Address = AddressSerializer(source='address', many=False, required=False, allow_null=True)

    def create(self, ahj, validated_data):
        address_data = None
        if validated_data.get('address') is not None:
            address_data = validated_data.pop('address')

        # Do not specify an id for a new contact record
        if validated_data.get('id') is not None:
            validated_data.pop('id')

        contact = Contact.objects.create(AHJ=ahj, **validated_data)

        if address_data is not None:
            AddressSerializer().create(contact, 'Contact', address_data)
        return contact

    def update(self, instance, validated_data):
        instance.ContactType = validated_data.get('ContactType', instance.ContactType)
        instance.Description = validated_data.get('Description', instance.Description)
        instance.Email = validated_data.get('Email', instance.Email)
        instance.FirstName = validated_data.get('FirstName', instance.FirstName)
        instance.HomePhone = validated_data.get('HomePhone', instance.HomePhone)
        instance.LastName = validated_data.get('LastName', instance.LastName)
        instance.MiddleName = validated_data.get('MiddleName', instance.MiddleName)
        instance.MobilePhone = validated_data.get('MobilePhone', instance.MobilePhone)
        instance.WorkPhone = validated_data.get('WorkPhone', instance.WorkPhone)
        instance.save()

        if validated_data.get('address') is not None:
            address_data = validated_data.pop('address')
            contact_address = Address.objects.filter(Contact=instance).first()
            if contact_address is None:
                AddressSerializer().create(instance, 'Contact', address_data)
            else:
                AddressSerializer().update(contact_address, address_data)
        return instance


class EngineeringReviewRequirementSerializer(serializers.Serializer):
    EngineeringReviewRequirementID = OrangeButtonIntegerFieldSerializer(source='id', required=False)
    RequirementLevel = OrangeButtonCharFieldSerializer(required=False)
    StampType = OrangeButtonCharFieldSerializer(required=False)
    Description = OrangeButtonCharFieldSerializer(required=False)
    EngineeringReviewType = OrangeButtonCharFieldSerializer(required=False)

    def create(self, ahj, validated_data):
        # Do not specify an id for a new engRevReq record
        if validated_data.get('id') is not None:
            validated_data.pop('id')
        eng_rev_req = EngineeringReviewRequirement.objects.create(AHJ=ahj, **validated_data)
        # create_edits(eng_rev_req, edit)
        return eng_rev_req

    def update(self, instance, validated_data):
        instance.Description = validated_data.get('Description', instance.Description)
        instance.EngineeringReviewType = validated_data.get('EngineeringReviewType', instance.EngineeringReviewType)
        instance.RequirementLevel = validated_data.get('RequirementLevel', instance.RequirementLevel)
        instance.StampType = validated_data.get('StampType', instance.StampType)
        instance.save()
        return instance


class AHJSerializer(serializers.Serializer):
    AHJID = OrangeButtonCharFieldSerializer(required=False)
    AHJName = OrangeButtonCharFieldSerializer(required=False)
    BuildingCode = OrangeButtonCharFieldSerializer(required=False)
    BuildingCodeNotes = OrangeButtonCharFieldSerializer(required=False)
    Description = OrangeButtonCharFieldSerializer(required=False)
    DocumentSubmissionMethod = OrangeButtonCharFieldSerializer(required=False)
    DocumentSubmissionMethodNotes = OrangeButtonCharFieldSerializer(required=False)
    ElectricCode = OrangeButtonCharFieldSerializer(required=False)
    ElectricCodeNotes = OrangeButtonCharFieldSerializer(required=False)
    FireCode = OrangeButtonCharFieldSerializer(required=False)
    FireCodeNotes = OrangeButtonCharFieldSerializer(required=False)
    ResidentialCode = OrangeButtonCharFieldSerializer(required=False)
    ResidentialCodeNotes = OrangeButtonCharFieldSerializer(required=False)
    WindCode = OrangeButtonCharFieldSerializer(required=False)
    WindCodeNotes = OrangeButtonCharFieldSerializer(required=False)
    Address = AddressSerializer(source='address', many=False, required=False, allow_null=True)
    Contacts = ContactSerializer(source='contact_set', many=True, required=False)
    EngineeringReviewRequirements = EngineeringReviewRequirementSerializer(source='engineeringreviewrequirement_set', many=True, required=False)

    def create(self, validated_data, edit):
        address_data = None
        contacts_data = None
        engineering_review_requirements_data = None
        if validated_data.get('AHJID') is not None:
            validated_data.pop('AHJID')
        if validated_data.get('address') is not None:
            address_data = validated_data.pop('address')
        if validated_data.get('contact_set') is not None:
            contacts_data = validated_data.pop('contact_set')
        if validated_data.get('engineeringreviewrequirement_set') is not None:
            engineering_review_requirements_data = validated_data.pop('engineeringreviewrequirement_set')

        ahj = AHJ.objects.create(**validated_data)
        edit.RecordID = ahj.AHJID
        edit.save()
        add_create_edits(ahj, edit)

        if address_data is not None:
            AddressSerializer().create(ahj, 'AHJ', address_data, edit)

        if contacts_data is not None:
            contact_serializer = ContactSerializer()
            for contact_data in contacts_data:
                contact_serializer.create(ahj, contact_data)

        if engineering_review_requirements_data is not None:
            engineering_review_requirement_serializer = EngineeringReviewRequirementSerializer()
            for engineering_review_requirement_data in engineering_review_requirements_data:
                engineering_review_requirement_serializer.create(ahj, engineering_review_requirement_data)

        return ahj

    def update(self, instance, validated_data):
        # Do not update if nothing was changed. self.data is current, self.initial_data is update
        if JSONRenderer().render(self.data) == JSONRenderer().render(self.initial_data):
            return instance

        instance.AHJName = validated_data.get('AHJName', instance.AHJName)
        instance.BuildingCode = validated_data.get('BuildingCode', instance.BuildingCode)
        instance.BuildingCodeNotes = validated_data.get('BuildingCodeNotes', instance.BuildingCodeNotes)
        instance.Description = validated_data.get('Description', instance.Description)
        instance.DocumentSubmissionMethod = validated_data.get('DocumentSubmissionMethod', instance.DocumentSubmissionMethod)
        instance.DocumentSubmissionMethodNotes = validated_data.get('DocumentSubmissionMethodNotes', instance.DocumentSubmissionMethodNotes)
        instance.ElectricCode = validated_data.get('ElectricCode', instance.ElectricCode)
        instance.ElectricCodeNotes = validated_data.get('ElectricCodeNotes', instance.ElectricCodeNotes)
        instance.FireCode = validated_data.get('FireCode', instance.FireCode)
        instance.FireCodeNotes = validated_data.get('FireCodeNotes', instance.FireCodeNotes)
        instance.ResidentialCode = validated_data.get('ResidentialCode', instance.ResidentialCode)
        instance.ResidentialCodeNotes = validated_data.get('ResidentialCodeNotes', instance.ResidentialCodeNotes)
        instance.save()

        if validated_data.get('address') is not None:
            address_data = validated_data.pop('address')
            ahj_address = Address.objects.filter(AHJ=instance).first()
            if ahj_address is None:
                AddressSerializer().create(instance, 'AHJ', address_data)
            else:
                AddressSerializer().update(ahj_address, address_data)

        if validated_data.get('contact_set') is not None:
            # Get array of submitted contacts
            contacts_data = validated_data.pop('contact_set')
            contact_serializer = ContactSerializer()
            # Get array of existing contacts of this AHJ
            ahj_contacts = Contact.objects.filter(AHJ=instance)
            # Identify contacts by id, and update the existing ones associated with this AHJ
            # Otherwise, create a new contact record for the AHJ
            for i in range(len(contacts_data)):
                contact_id = contacts_data[i].get('id')
                if contact_id is not None:
                    # There exists some contact with the submitted id
                    contact = ahj_contacts.filter(pk=contact_id).first()
                    if contact is None:
                        # The existing contact is not associated with this AHJ, so make a new one
                        contact_serializer.create(instance, contacts_data[i])
                    else:
                        # The existing contact is associated with this AHJ, so update it
                        contact_serializer.update(contact, contacts_data[i])
                else:
                    # There exists no contact with the submitted id, so make a new one
                    contact_serializer.create(instance, contacts_data[i])

        if validated_data.get('engineeringreviewrequirement_set') is not None:
            engineering_review_requirements_data = validated_data.pop('engineeringreviewrequirement_set')
            engineering_review_requirement_serializer = EngineeringReviewRequirementSerializer()
            ahj_eng_rev_req = EngineeringReviewRequirement.objects.filter(AHJ=instance)
            # Identify engRevReq by id, and update the existing ones associated with this AHJ
            # Otherwise, create a new engRevReq record for the AHJ
            for i in range(len(engineering_review_requirements_data)):
                eng_rev_req_id = engineering_review_requirements_data[i].get('id')
                if eng_rev_req_id is not None:
                    # There exists some engRevReq with the submitted id
                    eng_rev_req = ahj_eng_rev_req.filter(pk=eng_rev_req_id).first()
                    if eng_rev_req is None:
                        # The existing engRevReq is not associated with this AHJ, so make a new one
                        engineering_review_requirement_serializer.create(instance, engineering_review_requirements_data[i])
                    else:
                        # The existing engRevReq is associated with this AHJ, so update it
                        engineering_review_requirement_serializer.update(eng_rev_req, engineering_review_requirements_data[i])
                else:
                    # There exists no engRevReq with the submitted id, so make a new one
                    engineering_review_requirement_serializer.create(instance, engineering_review_requirements_data[i])

        return instance

    def __delete__(self, instance, edit):
        ahj_address = Address.objects.filter(AHJ=instance).first()
        if ahj_address is not None:
            AddressSerializer().__delete__(ahj_address, edit)
        instance.delete()


class EditSerializer(serializers.ModelSerializer):
    RecordID = serializers.CharField(required=False)
    PreviousValue = serializers.CharField(required=False)
    FieldName = serializers.CharField(required=False)
    Value = serializers.CharField(required=False)
    ModifyingUserID = serializers.IntegerField(required=False)
    ModifiedDate = serializers.DateTimeField(required=False)

    class Meta:
        model = Edit
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email_address'
        ]


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


def add_create_edits(record, edit):
    for attr, value in record.__dict__.items():
        if attr == '_state' or attr == 'id' or attr == 'AHJID':
            continue
        if value is not None and value != '':
            if record.__class__.__name__ == 'AHJ':
                Edit.objects.create(RecordID=record.AHJID, RecordType=record.__class__.__name__, EditType='update', FieldName=attr,
                                    Value=value, ModifyingUserID=edit.ModifyingUserID, ModifiedDate=edit.ModifiedDate,
                                    IsConfirmed=True, ConfirmingUserID=edit.ConfirmingUserID, ConfirmedDate=edit.ConfirmedDate)
            else:
                Edit.objects.create(RecordID=record.id, RecordType=record.__class__.__name__, EditType='update', FieldName=attr,
                                    Value=value, ModifyingUserID=edit.ModifyingUserID, ModifiedDate=edit.ModifiedDate,
                                    IsConfirmed=True, ConfirmingUserID=edit.ConfirmingUserID, ConfirmedDate=edit.ConfirmedDate)


def add_delete_edits(record, edit):
    # The record will never be an AHJ record
    Edit.objects.create(RecordID=record.id, RecordType=record.__class__.__name__, EditType='delete', ModifyingUserID=edit.ModifyingUserID,
                        ModifiedDate=edit.ModifiedDate, IsConfirmed=True, ConfirmingUserID=edit.ConfirmingUserID,
                        ConfirmedDate=edit.ConfirmedDate)

