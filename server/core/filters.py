import rest_framework_filters as filters
from .models import *
from django_filters import rest_framework as df_filters
from rest_framework import filters as rf_filters


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
            print(value)
            value = int(value[0])
            return self.NumberFilter.filter(qs, value)
        except ValueError:
            try:
                value = uuid.UUID(value[0])
                return self.UUIDFilter.filter(qs, value)
            except ValueError:
                return qs


class AHJFilter(filters.FilterSet, rf_filters.SearchFilter):
    AHJID__in = df_filters.UUIDFilter(field_name='AHJID')
    BuildingCode__in = CharInFilter(field_name='BuildingCode', lookup_expr='in')
    ElectricCode__in = CharInFilter(field_name='ElectricCode', lookup_expr='in')
    FireCode__in = CharInFilter(field_name='FireCode', lookup_expr='in')
    ResidentialCode__in = CharInFilter(field_name='ResidentialCode', lookup_expr='in')
    City__in = df_filters.CharFilter(field_name='address__City', lookup_expr='icontains')
    County__in = df_filters.CharFilter(field_name='address__County', lookup_expr='icontains')
    Country__in = df_filters.CharFilter(field_name='address__Country', lookup_expr='icontains')
    StateProvince__in = df_filters.CharFilter(field_name='address__StateProvince', lookup_expr='icontains')
    ZipPostalCode__in = df_filters.CharFilter(field_name='address__ZipPostalCode', lookup_expr='icontains')

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
