from django.urls import path, include

from . import views

urlpatterns = [
    path('location/', views.find_ahj_location, name='location'),
    path('address/', views.find_ahj_address, name='address')
]
