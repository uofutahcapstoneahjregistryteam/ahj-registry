from django.urls import path, include
from . import views


urlpatterns = [
    path('ahj/', views.AHJList.as_view(), name="ahj"),
    path('submit_edit/', views.submit_edit, name='change'),
    path('modify_edit/', views.modify_edit, name='change'),
    path('ahj_csv/', views.ahj_upload, name="upload"),
    path('geo/', include('ahj_gis.urls')),
    path('ahj/<uuid:AHJID>/', views.AHJDetail.as_view(), name="ahj"),
    path('contact/<str:pk>/', views.ContactDetail.as_view(), name="ahj"),
    path('eng-rev-req/<str:pk>/', views.EngineeringReviewRequirementDetail.as_view(), name="ahj"),
    path('history/ahj/', views.AHJHistory.as_view(), name="history"),
    path('history/ahj/<uuid:AHJID>/', views.AHJHistory.as_view(), name="history"),
    path('history/address/', views.AddressHistory.as_view(), name="history-address"),
    path('history/contact/', views.ContactHistory.as_view(), name="history-contact"),
    path('history/eng-rev-req/', views.EngineeringReviewRequirementHistory.as_view(), name="history-eng-rev-req"),
    path('history/location/', views.LocationHistory.as_view(), name="history-location"),
    path('login/', views.ObtainAuthTokenUserInfo.as_view(), name='api-token-auth')
]
