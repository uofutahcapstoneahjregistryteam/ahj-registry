from django.contrib.gis.db import models


"""
    Census shapefile polygon model
    
    How to differentiate County and Place:
        If len(GEOID) == 5, then it is a County
        If len(GEOID) == 7, then it is a Place
        
    POLYFP accomodates for COUNTYFP and PLACEFP
    POLYNS accomodates for COUNTYNS and PLACENS
"""
class Polygon(models.Model):
    STATEFP = models.CharField(max_length=2)
    STATEABBR = models.CharField(max_length=2, default='')
    POLYFP = models.CharField(max_length=5)
    POLYNS = models.CharField(max_length=8)
    GEOID = models.CharField(max_length=7)
    NAME = models.CharField(max_length=100)
    NAMELSAD = models.CharField(max_length=100)
    LSAD = models.CharField(max_length=2)
    CLASSFP = models.CharField(max_length=2)
    MTFCC = models.CharField(max_length=5)
    FUNCSTAT = models.CharField(max_length=1)
    ALAND = models.BigIntegerField()
    AWATER = models.BigIntegerField()
    INTPTLAT = models.CharField(max_length=11)
    INTPTLON = models.CharField(max_length=12)

    mpoly = models.MultiPolygonField()

    # County shapefile unique
    CSAFP = models.CharField(default='', max_length=3)
    CBSAFP = models.CharField(default='', max_length=5)
    METDIVFP = models.CharField(default='', max_length=5)

    # Place shapefile unique
    PCICBSA = models.CharField(default='', max_length=1)
    PCINECTA = models.CharField(default='', max_length=1)

    def __str__(self):
        return self.NAMELSAD + ', ' + self.STATEABBR


# Census county shapefile model
class County(models.Model):
    STATEFP = models.CharField(max_length=2)
    STATEABBR = models.CharField(max_length=2, default='')
    COUNTYFP = models.CharField(max_length=3)
    COUNTYNS = models.CharField(max_length=8)
    GEOID = models.CharField(max_length=5)
    NAME = models.CharField(max_length=100)
    NAMELSAD = models.CharField(max_length=100)
    LSAD = models.CharField(max_length=2)
    CLASSFP = models.CharField(max_length=2)
    MTFCC = models.CharField(max_length=5)
    CSAFP = models.CharField(max_length=3)
    CBSAFP = models.CharField(max_length=5)
    METDIVFP = models.CharField(max_length=5)
    FUNCSTAT = models.CharField(max_length=1)
    ALAND = models.BigIntegerField()
    AWATER = models.BigIntegerField()
    INTPTLAT = models.CharField(max_length=11)
    INTPTLON = models.CharField(max_length=12)

    mpoly = models.MultiPolygonField()

    def __str__(self):
        return self.NAMELSAD + ', ' + self.STATEABBR


# Census place shapefile model
class City(models.Model):
    STATEFP = models.CharField(max_length=2)
    STATEABBR = models.CharField(max_length=2, default='')
    PLACEFP = models.CharField(max_length=5)
    PLACENS = models.CharField(max_length=8)
    GEOID = models.CharField(max_length=7)
    NAME = models.CharField(max_length=100)
    NAMELSAD = models.CharField(max_length=100)
    LSAD = models.CharField(max_length=2)
    CLASSFP = models.CharField(max_length=2)
    PCICBSA = models.CharField(max_length=1)
    PCINECTA = models.CharField(max_length=1)
    MTFCC = models.CharField(max_length=5)
    FUNCSTAT = models.CharField(max_length=1)
    ALAND = models.BigIntegerField()
    AWATER = models.BigIntegerField()
    INTPTLAT = models.CharField(max_length=11)
    INTPTLON = models.CharField(max_length=12)

    mpoly = models.MultiPolygonField()

    def __str__(self):
        return self.NAMELSAD + ', ' + self.STATEABBR
