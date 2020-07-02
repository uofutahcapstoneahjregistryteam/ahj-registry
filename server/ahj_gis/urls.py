from django.urls import path, include

from . import views

urlpatterns = [
    path('coordinate/', views.find_ahj_coordinate, name='coordinate'),
    path('address/', views.find_ahj_address, name='address'),
    path('csv-county/', views.county_csv, name='csv-county'),
    path('csv-city/', views.city_csv, name='csv-city')
]
