import os
from django.contrib.gis.utils import LayerMapping
from .models import *

county_mapping = {
    'STATEFP': 'STATEFP',
    'COUNTYFP': 'COUNTYFP',
    'COUNTYNS': 'COUNTYNS',
    'GEOID': 'GEOID',
    'NAME': 'NAME',
    'NAMELSAD': 'NAMELSAD',
    'LSAD': 'LSAD',
    'CLASSFP': 'CLASSFP',
    'MTFCC': 'MTFCC',
    'CSAFP': 'CSAFP',
    'CBSAFP': 'CBSAFP',
    'METDIVFP': 'METDIVFP',
    'FUNCSTAT': 'FUNCSTAT',
    'ALAND': 'ALAND',
    'AWATER': 'AWATER',
    'INTPTLAT': 'INTPTLAT',
    'INTPTLON': 'INTPTLON',
    'mpoly': 'MULTIPOLYGON'
}

county_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', 'tl_2019_us_county/tl_2019_us_county.shp'),
)

city_mapping = {
    'STATEFP': 'STATEFP',
    'PLACEFP': 'PLACEFP',
    'PLACENS': 'PLACENS',
    'GEOID': 'GEOID',
    'NAME': 'NAME',
    'NAMELSAD': 'NAMELSAD',
    'LSAD': 'LSAD',
    'CLASSFP': 'CLASSFP',
    'PCICBSA': 'PCICBSA',
    'PCINECTA': 'PCINECTA',
    'MTFCC': 'MTFCC',
    'FUNCSTAT': 'FUNCSTAT',
    'ALAND': 'ALAND',
    'AWATER': 'AWATER',
    'INTPTLAT': 'INTPTLAT',
    'INTPTLON': 'INTPTLON',
    'mpoly': 'MULTIPOLYGON'
}

city_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', 'alaska/tl_2019_02_place.shp'),
)


def run_county(verbose=True):
    lm = LayerMapping(County, county_shp, county_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)


def run_city(path):
    lm = LayerMapping(City, os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', path),), city_mapping, transform=False)
    lm.save(strict=True, verbose=True)
