from django.contrib.gis.geos import Point
from .models import *
from core.models import AHJ


def get_ahj_set(longitude, latitude):
    coordinate = Point(float(longitude), float(latitude))

    # Filter by intersects
    city_set = City.objects.filter(mpoly__intersects=coordinate)
    county_set = County.objects.filter(mpoly__intersects=coordinate)

    city_names = []
    county_names = []

    # Filter intersects results by covers
    for city in city_set:
        # # Use covers to include coordinates on borders
        if city.mpoly.covers(coordinate):
            city_names.append(city.NAME)
    for county in county_set:
        # Use covers to include coordinates on borders
        if county.mpoly.covers(coordinate):
            county_names.append(county.NAME)

    # Combine all of the AHJ's with the found names into one QuerySet
    ahj_set = AHJ.objects.none()
    for name in city_names:
        ahj_set |= AHJ.objects.filter(address__City__icontains=name)
    for name in county_names:
        ahj_set |= AHJ.objects.filter(address__County__icontains=name)

    return ahj_set
