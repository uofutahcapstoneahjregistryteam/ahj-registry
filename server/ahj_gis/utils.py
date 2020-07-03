from django.contrib.gis.geos import Point
from .models import *
from core.models import AHJ, Address
import csv


def get_ahj_set(longitude, latitude):
    coordinate = Point(float(longitude), float(latitude))

    # Filter by intersects
    first_city_set = City.objects.filter(mpoly__intersects=coordinate)
    first_county_set = County.objects.filter(mpoly__intersects=coordinate)

    second_city_set = []
    second_county_set = []
    # Filter intersects results by covers
    for city in first_city_set:
        # # Use covers to include coordinates on borders
        if city.mpoly.covers(coordinate):
            second_city_set.append(city)
    for county in first_county_set:
        # Use covers to include coordinates on borders
        if county.mpoly.covers(coordinate):
            second_county_set.append(county)

    # Combine all of the AHJ's with the found names into one QuerySet
    ahj_set = []
    for city in second_city_set:
        ahj_set.append(AHJ.objects.get(city_mpoly=city))
    for county in second_county_set:
        ahj_set.append(AHJ.objects.get(county_mpoly=county))

    return ahj_set


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
        elif poly.STATEFP == '84': poly.STATEABBR = '84'
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
        elif poly.STATEFP == '71': poly.STATEABBR = '71'
        elif poly.STATEFP == '27': poly.STATEABBR = 'MN'
        elif poly.STATEFP == '28': poly.STATEABBR = 'MS'
        elif poly.STATEFP == '29': poly.STATEABBR = 'MO'
        elif poly.STATEFP == '30': poly.STATEABBR = 'MT'
        elif poly.STATEFP == '76': poly.STATEABBR = '76'
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
        elif poly.STATEFP == '95': poly.STATEABBR = '95'
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
        elif poly.STATEFP == '79': poly.STATEABBR = '79'
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
        elif poly.STATEFP == '84': poly.STATEABBR = '84'
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
        elif poly.STATEFP == '71': poly.STATEABBR = '71'
        elif poly.STATEFP == '27': poly.STATEABBR = 'MN'
        elif poly.STATEFP == '28': poly.STATEABBR = 'MS'
        elif poly.STATEFP == '29': poly.STATEABBR = 'MO'
        elif poly.STATEFP == '30': poly.STATEABBR = 'MT'
        elif poly.STATEFP == '76': poly.STATEABBR = '76'
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
        elif poly.STATEFP == '95': poly.STATEABBR = '95'
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
        elif poly.STATEFP == '79': poly.STATEABBR = '79'
        elif poly.STATEFP == '53': poly.STATEABBR = 'WA'
        elif poly.STATEFP == '54': poly.STATEABBR = 'WV'
        elif poly.STATEFP == '55': poly.STATEABBR = 'WI'
        elif poly.STATEFP == '56': poly.STATEABBR = 'WY'
        else:
            print(poly.STATEFP)
        poly.save()


def add_polygons():
    # Sort AHJs to at least make cure they are grouped by state.
    ahjs = AHJ.objects.filter(county_mpoly=None).filter(city_mpoly=None).order_by('address__StateProvince')
    counties = County.objects.all()
    cities = City.objects.all()

    i = 1
    # Counter for how many times we refiltered by state
    state_refilter_count = 1

    with open('potential_duplicates.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['AHJID', 'AHJName', 'StateProvince', 'AddedToBoth'])

        # Track what state we should filter for
        current_state_abbr = Address.objects.get(AHJ=ahjs.first()).StateProvince

        # Hold the counties and places of the current state
        temp_counties = counties.filter(STATEABBR=current_state_abbr).order_by('NAMELSAD')
        temp_cities = cities.filter(STATEABBR=current_state_abbr).order_by('NAMELSAD')

        # For each ahj, give it a place and/or county
        # Record the ahjs that are potential duplicates
        for ahj in ahjs:

            # Counter to check if both place and county were assigned to an ahj
            added_to_both = 0

            # Get the ahj's address to filter by state
            address = Address.objects.get(AHJ=ahj)

            # Check if we need to filter by another state now
            temp_state_abbr = address.StateProvince
            if current_state_abbr != temp_state_abbr:
                current_state_abbr = temp_state_abbr
                temp_counties = counties.filter(STATEABBR=current_state_abbr).order_by('NAMELSAD')
                temp_cities = cities.filter(STATEABBR=current_state_abbr).order_by('NAMELSAD')
                print('Refilter by state %i for %s' % (state_refilter_count, current_state_abbr))
                state_refilter_count += 1

            county = None
            city = None
            county_index = binary_search(temp_counties, ahj.AHJName)
            city_index = binary_search(temp_cities, ahj.AHJName)

            if county_index != -1:
                county = temp_counties[county_index]
            if city_index != -1:
                city = temp_cities[city_index]

            if county is not None:
                if ahj.county_mpoly is not None:
                    # Write potential duplicates
                    writer.writerow([ahj.AHJID, ahj.AHJName, address.StateProvince])
                else:
                    ahj.county_mpoly = county
                    ahj.save()
                    print('Set county ' + county.NAMELSAD + ', ' + county.STATEABBR + ' as the polygon for ' + ahj.AHJName)
                    added_to_both += 1

            if city is not None:
                if ahj.city_mpoly is not None:
                    # Write potential duplicates
                    writer.writerow([ahj.AHJID, ahj.AHJName, address.StateProvince])
                else:
                    ahj.city_mpoly = city
                    ahj.save()
                    print('Set city ' + city.NAMELSAD + ', ' + city.STATEABBR + ' as the polygon for ' + ahj.AHJName)
                    added_to_both += 1

            print('AHJ %i done' % i)
            i += 1
            if added_to_both == 2:
                writer.writerow([ahj.AHJID, ahj.AHJName, address.StateProvince, 'True'])


def clear_ahj_polygon_assignment():
    ahjs = AHJ.objects.all().order_by('address__StateProvince')
    i = 1
    for ahj in ahjs:
        ahj.county_mpoly = None
        ahj.city_mpoly = None
        ahj.save()
        print('Cleared mpoly of ' + ahj.AHJName)
        print('AHJ %i done' % i)
        i += 1


# Iterative Binary Search Function
# It returns index of x in given array arr if present,
# else returns -1
def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    mid = 0
    x = x.lower()

    while low <= high:
        mid = (high + low) // 2
        # Check if x is present at mid
        if arr[mid].NAMELSAD.lower() < x:
            low = mid + 1

        # If x is greater, ignore left half
        elif arr[mid].NAMELSAD.lower() > x:
            high = mid - 1

        # If x is smaller, ignore right half
        else:
            return mid

            # If we reach here, then the element was not present
    return -1
