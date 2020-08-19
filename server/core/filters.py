import rest_framework_filters as filters
from .models import *
from django_filters import rest_framework as df_filters
from rest_framework import filters as rf_filters
from ahj_gis import utils as ahj_gis_utils
from googlemaps import Client
from ahj_gis.constants import GOOGLE_GEOCODING_API_KEY

gmaps = Client(key=GOOGLE_GEOCODING_API_KEY)


class CharInFilter(df_filters.BaseInFilter, df_filters.CharFilter):
    pass


class NullBooleanFilter(df_filters.BooleanFilter):
    def filter(self, qs, value):
        if value is None:
            return qs.filter(IsConfirmed=None)
        return super().filter(qs, value)


class RecordIDFilter(df_filters.BaseInFilter):
    def __init__(self, field_name):
        self.field_name = field_name
        self.NumberFilter = df_filters.NumberFilter(field_name=field_name)
        self.UUIDFilter = df_filters.UUIDFilter(field_name=field_name)
        super().__init__(field_name)

    def filter(self, qs, value):
        try:
            value = int(value[0])
            return self.NumberFilter.filter(qs, value)
        except ValueError:
            try:
                value = uuid.UUID(value[0])
                return self.UUIDFilter.filter(qs, value)
            except ValueError:
                return qs


class LocationFilter(df_filters.BaseInFilter):
    def filter(self, qs, value):
        try:
            longitude = float(value[0])
            latitude = float(value[1])
            return ahj_gis_utils.filter_ahjs_by_location(longitude, latitude, ahjs_to_search=qs)
        except ValueError:
            return qs


class AddressFilter(df_filters.BaseInFilter):
    def filter(self, qs, value):
        address = ''
        for string in value:
            address += string
        geocode_result = gmaps.geocode(address)
        if len(geocode_result) == 0:
            return qs
        ahj_qs = AHJ.objects.none()
        for x in range(len(geocode_result)):
            coordinates = geocode_result[x]['geometry']['location']
            longitude = coordinates['lng']
            latitude = coordinates['lat']
            ahj_qs |= ahj_gis_utils.filter_ahjs_by_location(longitude, latitude, ahjs_to_search=qs)
        return ahj_qs


class AHJFilter(filters.FilterSet, rf_filters.SearchFilter):
    AHJID__in = df_filters.UUIDFilter(field_name='AHJID')
    BuildingCode__in = CharInFilter(field_name='BuildingCode', lookup_expr='in')
    ElectricCode__in = CharInFilter(field_name='ElectricCode', lookup_expr='in')
    FireCode__in = CharInFilter(field_name='FireCode', lookup_expr='in')
    ResidentialCode__in = CharInFilter(field_name='ResidentialCode', lookup_expr='in')
    WindCode__in = CharInFilter(field_name='WindCode', lookup_expr='in')
    Location__in = LocationFilter()
    Address__in = AddressFilter()

    class Meta:
        model = AHJ
        fields = '__all__'


class EditFilter(filters.FilterSet, rf_filters.SearchFilter):
    RecordID__in = RecordIDFilter(field_name='RecordID')
    ModifyingUserID__in = df_filters.NumberFilter(field_name='ModifyingUserID')
    ConfirmingUserID__in = df_filters.NumberFilter(field_name='ConfirmingUserID')
    IsConfirmed__in = NullBooleanFilter(field_name='IsConfirmed')

    class Meta:
        model = Edit
        fields = '__all__'
