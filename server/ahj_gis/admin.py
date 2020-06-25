from django.contrib.gis import admin
from .models import *

# Register your models here.
admin.site.register(County, admin.OSMGeoAdmin)
admin.site.register(City, admin.OSMGeoAdmin)
