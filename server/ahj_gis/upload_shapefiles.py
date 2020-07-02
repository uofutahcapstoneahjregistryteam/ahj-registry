import os
from django.contrib.gis.utils import LayerMapping
from core.models import AHJ, Address
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


def run_county(verbose=True):
    lm = LayerMapping(County, county_shp, county_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)


def run_city():
    lm = LayerMapping(City, os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', city_shp),), city_mapping, transform=False)
    lm.save(strict=True, verbose=True)


def add_state_abbr():
    counties = County.objects.all()
    cities = City.objects.all()
    for poly in counties:
        if poly.STATEFP == '01': poly.STATEABBR = 'AL'
        elif poly.STATEFP == '02': poly.STATEABBR = 'AK'
        elif poly.STATEFP == '60': poly.STATEABBR = 'AS'
        elif poly.STATEFP == '04': poly.STATEABBR = 'AZ'
        elif poly.STATEFP == '05': poly.STATEABBR = 'AR'
        elif poly.STATEFP == '81': poly.STATEABBR = 'BI'
        elif poly.STATEFP == '06': poly.STATEABBR = 'CA'
        elif poly.STATEFP == '08': poly.STATEABBR = 'CO'
        elif poly.STATEFP == '09': poly.STATEABBR = 'CT'
        elif poly.STATEFP == '10': poly.STATEABBR = 'DE'
        elif poly.STATEFP == '11': poly.STATEABBR = 'DC'
        elif poly.STATEFP == '12': poly.STATEABBR = 'FL'
        elif poly.STATEFP == '64': poly.STATEABBR = 'FM'
        elif poly.STATEFP == '13': poly.STATEABBR = 'GA'
        elif poly.STATEFP == '66': poly.STATEABBR = 'GU'
        elif poly.STATEFP == '15': poly.STATEABBR = 'HI'
        elif poly.STATEFP == '84': poly.STATEABBR = 'HI'
        elif poly.STATEFP == '16': poly.STATEABBR = 'ID'
        elif poly.STATEFP == '17': poly.STATEABBR = 'IL'
        elif poly.STATEFP == '18': poly.STATEABBR = 'IN'
        elif poly.STATEFP == '19': poly.STATEABBR = 'IA'
        elif poly.STATEFP == '86': poly.STATEABBR = 'JI'
        elif poly.STATEFP == '67': poly.STATEABBR = 'JA'
        elif poly.STATEFP == '20': poly.STATEABBR = 'KS'
        elif poly.STATEFP == '21': poly.STATEABBR = 'KY'
        elif poly.STATEFP == '89': poly.STATEABBR = 'KR'
        elif poly.STATEFP == '22': poly.STATEABBR = 'LA'
        elif poly.STATEFP == '23': poly.STATEABBR = 'ME'
        elif poly.STATEFP == '68': poly.STATEABBR = 'MH'
        elif poly.STATEFP == '24': poly.STATEABBR = 'MD'
        elif poly.STATEFP == '25': poly.STATEABBR = 'MA'
        elif poly.STATEFP == '26': poly.STATEABBR = 'MI'
        elif poly.STATEFP == '71': poly.STATEABBR = 'MI'
        elif poly.STATEFP == '27': poly.STATEABBR = 'MN'
        elif poly.STATEFP == '28': poly.STATEABBR = 'MS'
        elif poly.STATEFP == '29': poly.STATEABBR = 'MO'
        elif poly.STATEFP == '30': poly.STATEABBR = 'MT'
        elif poly.STATEFP == '76': poly.STATEABBR = 'MI'
        elif poly.STATEFP == '31': poly.STATEABBR = 'NE'
        elif poly.STATEFP == '32': poly.STATEABBR = 'NV'
        elif poly.STATEFP == '33': poly.STATEABBR = 'NH'
        elif poly.STATEFP == '34': poly.STATEABBR = 'NJ'
        elif poly.STATEFP == '35': poly.STATEABBR = 'NM'
        elif poly.STATEFP == '36': poly.STATEABBR = 'NY'
        elif poly.STATEFP == '37': poly.STATEABBR = 'NC'
        elif poly.STATEFP == '38': poly.STATEABBR = 'ND'
        elif poly.STATEFP == '69': poly.STATEABBR = 'MP'
        elif poly.STATEFP == '39': poly.STATEABBR = 'OH'
        elif poly.STATEFP == '40': poly.STATEABBR = 'OK'
        elif poly.STATEFP == '41': poly.STATEABBR = 'OR'
        elif poly.STATEFP == '70': poly.STATEABBR = 'PW'
        elif poly.STATEFP == '95': poly.STATEABBR = 'PA'
        elif poly.STATEFP == '42': poly.STATEABBR = 'PA'
        elif poly.STATEFP == '72': poly.STATEABBR = 'PR'
        elif poly.STATEFP == '44': poly.STATEABBR = 'RI'
        elif poly.STATEFP == '45': poly.STATEABBR = 'SC'
        elif poly.STATEFP == '46': poly.STATEABBR = 'SD'
        elif poly.STATEFP == '47': poly.STATEABBR = 'TN'
        elif poly.STATEFP == '48': poly.STATEABBR = 'TX'
        elif poly.STATEFP == '74': poly.STATEABBR = 'UM'
        elif poly.STATEFP == '49': poly.STATEABBR = 'UT'
        elif poly.STATEFP == '50': poly.STATEABBR = 'VT'
        elif poly.STATEFP == '51': poly.STATEABBR = 'VA'
        elif poly.STATEFP == '78': poly.STATEABBR = 'VI'
        elif poly.STATEFP == '79': poly.STATEABBR = 'WI'
        elif poly.STATEFP == '53': poly.STATEABBR = 'WA'
        elif poly.STATEFP == '54': poly.STATEABBR = 'WV'
        elif poly.STATEFP == '55': poly.STATEABBR = 'WI'
        elif poly.STATEFP == '56': poly.STATEABBR = 'WY'
        else:
            print(poly.STATEFP)
        poly.save()
    for poly in cities:
        if poly.STATEFP == '01': poly.STATEABBR = 'AL'
        elif poly.STATEFP == '02': poly.STATEABBR = 'AK'
        elif poly.STATEFP == '60': poly.STATEABBR = 'AS'
        elif poly.STATEFP == '04': poly.STATEABBR = 'AZ'
        elif poly.STATEFP == '05': poly.STATEABBR = 'AR'
        elif poly.STATEFP == '81': poly.STATEABBR = 'BI'
        elif poly.STATEFP == '06': poly.STATEABBR = 'CA'
        elif poly.STATEFP == '08': poly.STATEABBR = 'CO'
        elif poly.STATEFP == '09': poly.STATEABBR = 'CT'
        elif poly.STATEFP == '10': poly.STATEABBR = 'DE'
        elif poly.STATEFP == '11': poly.STATEABBR = 'DC'
        elif poly.STATEFP == '12': poly.STATEABBR = 'FL'
        elif poly.STATEFP == '64': poly.STATEABBR = 'FM'
        elif poly.STATEFP == '13': poly.STATEABBR = 'GA'
        elif poly.STATEFP == '66': poly.STATEABBR = 'GU'
        elif poly.STATEFP == '15': poly.STATEABBR = 'HI'
        elif poly.STATEFP == '84': poly.STATEABBR = 'HI'
        elif poly.STATEFP == '16': poly.STATEABBR = 'ID'
        elif poly.STATEFP == '17': poly.STATEABBR = 'IL'
        elif poly.STATEFP == '18': poly.STATEABBR = 'IN'
        elif poly.STATEFP == '19': poly.STATEABBR = 'IA'
        elif poly.STATEFP == '86': poly.STATEABBR = 'JI'
        elif poly.STATEFP == '67': poly.STATEABBR = 'JA'
        elif poly.STATEFP == '20': poly.STATEABBR = 'KS'
        elif poly.STATEFP == '21': poly.STATEABBR = 'KY'
        elif poly.STATEFP == '89': poly.STATEABBR = 'KR'
        elif poly.STATEFP == '22': poly.STATEABBR = 'LA'
        elif poly.STATEFP == '23': poly.STATEABBR = 'ME'
        elif poly.STATEFP == '68': poly.STATEABBR = 'MH'
        elif poly.STATEFP == '24': poly.STATEABBR = 'MD'
        elif poly.STATEFP == '25': poly.STATEABBR = 'MA'
        elif poly.STATEFP == '26': poly.STATEABBR = 'MI'
        elif poly.STATEFP == '71': poly.STATEABBR = 'MI'
        elif poly.STATEFP == '27': poly.STATEABBR = 'MN'
        elif poly.STATEFP == '28': poly.STATEABBR = 'MS'
        elif poly.STATEFP == '29': poly.STATEABBR = 'MO'
        elif poly.STATEFP == '30': poly.STATEABBR = 'MT'
        elif poly.STATEFP == '76': poly.STATEABBR = 'MI'
        elif poly.STATEFP == '31': poly.STATEABBR = 'NE'
        elif poly.STATEFP == '32': poly.STATEABBR = 'NV'
        elif poly.STATEFP == '33': poly.STATEABBR = 'NH'
        elif poly.STATEFP == '34': poly.STATEABBR = 'NJ'
        elif poly.STATEFP == '35': poly.STATEABBR = 'NM'
        elif poly.STATEFP == '36': poly.STATEABBR = 'NY'
        elif poly.STATEFP == '37': poly.STATEABBR = 'NC'
        elif poly.STATEFP == '38': poly.STATEABBR = 'ND'
        elif poly.STATEFP == '69': poly.STATEABBR = 'MP'
        elif poly.STATEFP == '39': poly.STATEABBR = 'OH'
        elif poly.STATEFP == '40': poly.STATEABBR = 'OK'
        elif poly.STATEFP == '41': poly.STATEABBR = 'OR'
        elif poly.STATEFP == '70': poly.STATEABBR = 'PW'
        elif poly.STATEFP == '95': poly.STATEABBR = 'PA'
        elif poly.STATEFP == '42': poly.STATEABBR = 'PA'
        elif poly.STATEFP == '72': poly.STATEABBR = 'PR'
        elif poly.STATEFP == '44': poly.STATEABBR = 'RI'
        elif poly.STATEFP == '45': poly.STATEABBR = 'SC'
        elif poly.STATEFP == '46': poly.STATEABBR = 'SD'
        elif poly.STATEFP == '47': poly.STATEABBR = 'TN'
        elif poly.STATEFP == '48': poly.STATEABBR = 'TX'
        elif poly.STATEFP == '74': poly.STATEABBR = 'UM'
        elif poly.STATEFP == '49': poly.STATEABBR = 'UT'
        elif poly.STATEFP == '50': poly.STATEABBR = 'VT'
        elif poly.STATEFP == '51': poly.STATEABBR = 'VA'
        elif poly.STATEFP == '78': poly.STATEABBR = 'VI'
        elif poly.STATEFP == '79': poly.STATEABBR = 'WI'
        elif poly.STATEFP == '53': poly.STATEABBR = 'WA'
        elif poly.STATEFP == '54': poly.STATEABBR = 'WV'
        elif poly.STATEFP == '55': poly.STATEABBR = 'WI'
        elif poly.STATEFP == '56': poly.STATEABBR = 'WY'
        else:
            print(poly.STATEFP)
        poly.save()


def add_ahjs_to_polygons():
    ahjs = AHJ.objects.all().order_by('address__StateProvince', 'AHJName')
    print(Address.objects.get(AHJ=ahjs.first()).StateProvince + ' ' + ahjs.first().AHJName)
    print(Address.objects.get(AHJ=ahjs.last()).StateProvince + ' ' + ahjs.last().AHJName)
    counties = County.objects.all()
    cities = City.objects.all()
    i = 1
    state_refilter_count = 1
    both_string = ''
    current_state_abbr = Address.objects.get(AHJ=ahjs.first()).StateProvince
    temp_counties = counties.filter(STATEABBR=current_state_abbr)
    temp_cities = cities.filter(STATEABBR=current_state_abbr)
    for ahj in ahjs:
        added_to_both = 0
        address = Address.objects.get(AHJ=ahj)
        temp_state_abbr = address.StateProvince
        if current_state_abbr != temp_state_abbr:
            current_state_abbr = temp_state_abbr
            temp_counties = counties.filter(STATEABBR=current_state_abbr)
            temp_cities = cities.filter(STATEABBR=current_state_abbr)
            print('Refilter by state %i', state_refilter_count)
            state_refilter_count += 1
        county = temp_counties.filter(NAMELSAD__exact=ahj.AHJName)
        city = temp_cities.filter(NAMELSAD__exact=ahj.AHJName)

        if len(county) == 1:
            if ahj.county_mpoly is not None:
                print('AHJ ' + ahj.AHJName + ' already has county ' + ahj.county_mpoly.NAMELSAD + '. Did not reassign to ' + county.first().NAMELSAD)
            else:
                ahj.county_mpoly = county.first()
                ahj.save()
                print('Set county' + county.first().NAMELSAD + ' in ' + county.first().STATEABBR + ' as the polygon for ' + ahj.AHJName)
                added_to_both += 1
        elif len(county) > 1:
            print('Multiple counties in ' + address.StateProvince + ' with name ' + ahj.AHJName)

        if len(city) == 1:
            if ahj.city_mpoly is not None:
                print('AHJ ' + ahj.AHJName + ' already has county ' + ahj.city_mpoly.NAMELSAD + '. Did not reassign to ' + city.first().NAMELSAD)
            else:
                ahj.city_mpoly = city.first()
                ahj.save()
                print('Set city' + city.first().NAMELSAD + ' in ' + city.first().STATEABBR + ' as the polygon for ' + ahj.AHJName)
                added_to_both += 1
        elif len(city) > 1:
            print('Multiple cities in ' + address.StateProvince + ' with name ' + ahj.AHJName)
        print('AHJ %i done', i)
        i += 1
        if added_to_both == 2:
            both_string += ahj.AHJName + ', '
    print(both_string)


def clear_ahj_polygon_assignment():
    ahjs = AHJ.objects.all().order_by('address__StateProvince')
    i = 1
    for ahj in ahjs:
        ahj.county_mpoly = None
        ahj.city_mpoly = None
        ahj.save()
        print('Cleared mpoly of ' + ahj.AHJName)
        print('AHJ %i done', i)
        i += 1
