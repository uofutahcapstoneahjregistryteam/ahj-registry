from rest_framework.decorators import api_view
from .serializers import *
from rest_framework import generics
from .permissions import *
from rest_framework.response import Response
from .filters import *
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.views import ObtainAuthToken
from .utils import *

import csv, io
from django.shortcuts import render
from django.contrib import messages


def ahj_upload(request):
    # declaring template
    template = "ahj_upload.html"
    data = AHJ.objects.all()
    # prompt is a context variable that can have different values      depending on their context
    prompt = {
        'order': 'Order of the CSV should be state_abbr, (city|county)_name',
        'profiles': data
              }
    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, template, prompt)
    csv_file = request.FILES['file']
    # let's check if it is a csv file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    data_set = csv_file.read().decode('UTF-8')
    # setup a stream which is when we loop through each line we are able to handle a data in a stream
    io_string = io.StringIO(data_set)
    next(io_string)
    in_city = True
    i = 1
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        Address.objects.create(
            AHJ=AHJ.objects.create(AHJName=column[1]),
            StateProvince=column[0]
        )
        print(i)
        i += 1
    context = {}
    return render(request, template, context)


@api_view(['GET'])
def get_ahj_history(request, pk):
    if request.auth is None:
        return Response(request.detail)
    try:
        ahj = AHJ.objects.get(pk=pk)
    except AHJ.DoesNotExist:
        return Response({'detail': 'AHJ does not exist'})
    return get_ahj_diff(ahj)


@api_view(['POST'])
def submit_edit(request):
    if request.auth is None:
        return Response(request.detail)
    return create_edit(request)


@api_view(['GET'])
def edit_detail(request, pk):
    if request.auth is None:
        return Response(request.detail)
    return set_edit(request, pk)


class AHJList(generics.ListAPIView):
    queryset = AHJ.objects.all()
    serializer_class = AHJSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUserOrReadOnly)
    filter_class = AHJFilter
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['AHJName', 'address__City', 'address__County', 'address__Country', 'address__StateProvince', 'address__ZipPostalCode']

    def list(self, request):
        AHJ.confirmed_edits_only = False
        AHJ.highest_vote_rating = False
        view_mode = request.GET.get('view', '')
        if view_mode == 'confirmed':
            AHJ.confirmed_edits_only = True
        elif view_mode == 'highest_voted':
            AHJ.highest_vote_rating = True
        return super().list(self)


class AHJDetail(generics.RetrieveAPIView):
    lookup_field = 'AHJID'
    queryset = AHJ.objects.all()
    serializer_class = AHJSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUserOrReadOnly,)

    def get(self, request, *args, **kwargs):
        AHJ.confirmed_edits_only = False
        AHJ.highest_vote_rating = False
        view_mode = request.GET.get('view', '')
        if view_mode == 'confirmed':
            AHJ.confirmed_edits_only = True
        elif view_mode == 'highest_voted':
            AHJ.highest_vote_rating = True
        return super().get(self)


# class RecordEditsList(generics.RetrieveAPIView):
#     lookup_field = 'RecordID'
#     queryset = Edit.objects.filter(lookup_field).filter(IsConfirmed=None)
#     serializer_class = EditSerializer
#     permission_classes = (permissions.IsAuthenticated, IsSuperUserOrReadOnly)


class ContactDetail(generics.DestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUserOrReadOnly,)


class EngineeringReviewRequirementDetail(generics.DestroyAPIView):
    queryset = EngineeringReviewRequirement.objects.all()
    serializer_class = EngineeringReviewRequirementSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUserOrReadOnly,)


class AHJHistory(generics.ListCreateAPIView):
    lookup_field = 'AHJID'
    queryset = AHJ.history.all()
    serializer_class = AHJHistorySerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUserOrReadOnly)
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['AHJID', 'AHJName']


class AddressHistory(generics.ListCreateAPIView):
    queryset = Address.history.all()
    serializer_class = AddressHistorySerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUserOrReadOnly)
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['AHJ__AHJID', 'AHJ__AHJName', 'Contact__FirstName', 'Contact__MiddleName', 'Contact__LastName', 'Contact__id']


class ContactHistory(generics.ListCreateAPIView):
    queryset = Contact.history.all()
    serializer_class = ContactHistorySerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUserOrReadOnly)
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['AHJ__AHJID', 'FirstName', 'LastName', 'id']


class EngineeringReviewRequirementHistory(generics.ListCreateAPIView):
    queryset = EngineeringReviewRequirement.history.all()
    serializer_class = EngineeringReviewRequirementHistorySerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUserOrReadOnly)
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['AHJ__AHJID', 'EngineeringReviewType', 'RequirementLevel', 'StampType', 'id']


class LocationHistory(generics.ListCreateAPIView):
    queryset = Location.history.all()
    serializer_class = LocationHistorySerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperUserOrReadOnly)
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['Address__id']


class ObtainAuthTokenUserInfo(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(ObtainAuthTokenUserInfo, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({
                    'status': 'success',
                    'is_superuser': token.user.is_superuser,
                    'is_staff': token.user.is_staff,
                    'auth_token': token.key
                })
