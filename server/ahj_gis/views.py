from rest_framework.utils import json
from .utils import get_ahj_set
from rest_framework.decorators import api_view
from core.models import AHJ
from core.serializers import AHJSerializer
from rest_framework.response import Response
from core.serializers import AddressSerializer, LocationSerializer
import requests


@api_view(['POST'])
def find_ahj_coordinate(request):
    if request.auth is None:
        return Response(request.detail)

    longitude = ''
    latitude = ''

    if request.data.get('Location') is None:
        # The data is an Address
        location_serializer = LocationSerializer(data=request.data)
        if location_serializer.is_valid():
            validated_data = location_serializer.validated_data
            longitude = validated_data.get('Longitude', '')
            latitude = validated_data.get('Latitude', '')
    else:
        # The data is a Location
        address_serializer = AddressSerializer(data=request.data)
        if address_serializer.is_valid():
            validated_data = address_serializer.validated_data
            if validated_data.get('location') is not None:
                location = validated_data.pop('location')
                longitude = location.get('Longitude', '')
                latitude = location.get('Latitude', '')

    if longitude == '' or latitude == '':
        return Response({'detail': 'invalid coordinates'})

    ahj_set = get_ahj_set(longitude, latitude)

    return Response(AHJSerializer(ahj_set, many=True).data)


@api_view(['POST'])
def find_ahj_address(request):
    if request.auth is None:
        return Response(request.detail)
    street = request.data.get('AddrLine1', '')
    city = request.data.get('City', '')
    state = request.data.get('State', '')
    zip = request.data.get('Zip', '')
    census_url = 'https://geocoding.geo.census.gov/geocoder/locations/address'\
                 + '?street=' + street\
                 + '&city=' + city\
                 + '&state=' + state\
                 + '&zip=' + zip\
                 + '&benchmark=Public_AR_Current&format=json'
    census_call = requests.get(census_url)
    census_response = json.loads(census_call.content.decode())
    if census_call.status_code != 200:
        return Response(census_response)
    census_addresses = census_response['result']['addressMatches']
    if len(census_addresses) == 0:
        return Response({'detail': 'no coordinates were found for the given address'})

    # Find AHJ's for all possible address matches
    ahj_set = AHJ.objects.none()
    for census_address in census_addresses:
        coordinates = census_address['coordinates']
        longitude = coordinates['x']
        latitude = coordinates['y']
        ahj_set |= get_ahj_set(longitude, latitude)

    return Response(AHJSerializer(ahj_set, many=True).data)
