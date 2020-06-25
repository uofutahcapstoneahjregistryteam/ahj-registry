import rest_framework_filters as filters
from .models import *
from django_filters import rest_framework as df_filters
from rest_framework import filters as rf_filters


class CharInFilter(df_filters.BaseInFilter, df_filters.CharFilter):
    pass


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
