import os
from django.contrib.gis.utils import LayerMapping
from core.models import AHJ, Address
from .models import *


state_mapping = {
    'REGION': 'REGION',
    'DIVISION': 'DIVISION',
    'STATEFP': 'STATEFP',
    'STATENS': 'STATENS',
    'GEOID': 'GEOID',
    'STUSPS': 'STUSPS',
    'NAME': 'NAME',
    'LSAD': 'LSAD',
    'MTFCC': 'MTFCC',
    'FUNCSTAT': 'FUNCSTAT',
    'ALAND': 'ALAND',
    'AWATER': 'AWATER',
    'INTPTLAT': 'INTPTLAT',
    'INTPTLON': 'INTPTLON',
    'mpoly': 'MULTIPOLYGON'
}

state_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', 'tl_2019_us_state/tl_2019_us_state.shp'),
)


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

county_mapping10 = {
    'STATEFP': 'STATEFP10',
    'COUNTYFP': 'COUNTYFP10',
    'COUNTYNS': 'COUNTYNS10',
    'GEOID': 'GEOID10',
    'NAME': 'NAME10',
    'NAMELSAD': 'NAMELSAD10',
    'LSAD': 'LSAD10',
    'CLASSFP': 'CLASSFP10',
    'MTFCC': 'MTFCC10',
    'CSAFP': 'CSAFP10',
    'CBSAFP': 'CBSAFP10',
    'METDIVFP': 'METDIVFP10',
    'FUNCSTAT': 'FUNCSTAT10',
    'ALAND': 'ALAND10',
    'AWATER': 'AWATER10',
    'INTPTLAT': 'INTPTLAT10',
    'INTPTLON': 'INTPTLON10',
    'mpoly': 'MULTIPOLYGON'
}

county_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', 'tl_2010_02_county10/tl_2010_02_county10.shp'),
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

city_mapping10 = {
    'STATEFP': 'STATEFP10',
    'PLACEFP': 'PLACEFP10',
    'PLACENS': 'PLACENS10',
    'GEOID': 'GEOID10',
    'NAME': 'NAME10',
    'NAMELSAD': 'NAMELSAD10',
    'LSAD': 'LSAD10',
    'CLASSFP': 'CLASSFP10',
    'PCICBSA': 'PCICBSA10',
    'PCINECTA': 'PCINECTA10',
    'MTFCC': 'MTFCC10',
    'FUNCSTAT': 'FUNCSTAT10',
    'ALAND': 'ALAND10',
    'AWATER': 'AWATER10',
    'INTPTLAT': 'INTPTLAT10',
    'INTPTLON': 'INTPTLON10',
    'mpoly': 'MULTIPOLYGON'
}

city_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', 'tl_2010_02_place10/tl_2010_02_place10.shp'),
)


def run_state(verbose=True):
    lm = LayerMapping(State, state_shp, state_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)


def run_county(verbose=True):
    lm = LayerMapping(County, county_shp, county_mapping10, transform=False)
    lm.save(strict=True, verbose=verbose)


def run_city():
    lm = LayerMapping(City, os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', city_shp),), city_mapping10, transform=False)
    lm.save(strict=True, verbose=True)
