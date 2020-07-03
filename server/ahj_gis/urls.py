from django.urls import path, include

from . import views

urlpatterns = [
    path('coordinate/', views.find_ahj_coordinate, name='coordinate'),
    path('address/', views.find_ahj_address, name='address')
]
