from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from streetEvents.models import StreetEvent
from streetEvents.serializers import EventSerializer
from rest_framework.decorators import api_view
import datetime

from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import pyproj

@api_view(['GET'])
def event_comands_list(request):
    data = dict()
    data['Create'] = dict()
    data['Create']['command'] = 'http://127.0.0.1:8000/streetEvents/'
    data['Create']['body'] = '{"description": "","address": "","category": ""}'

    data['Get'] = dict()
    data['Get']['id'] = 'command: http://127.0.0.1:8000/streetEvents/id=?'
    data['Get']['category'] = 'command: http://127.0.0.1:8000/streetEvents/category=?'


    data['Update'] = dict()
    data['Update']['command'] = 'http://127.0.0.1:8000/streetEvents/category=?'
    data['Update']['body'] = '{"description": "","address": "","category": "", state: ""}'

    # GET list of events, POST a new events
    return JsonResponse(data, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT'])
def event_detail_id(request, id):
    # find tutorial by pk (id)
    try:
        event = StreetEvent.objects.get(pk=id)
    except StreetEvent.DoesNotExist:
        return JsonResponse({'message': 'The Event does not exist'}, status=status.HTTP_404_NOT_FOUND)
    event_serializer = EventSerializer(event)

    current_user = request.user

    # GET / PUT
    if request.method == 'GET':
        return JsonResponse(event_serializer.data)
    elif request.method == 'PUT':
        if request.user.is_authenticated:
            event_data = event_serializer.data
            event_data.update(JSONParser().parse(request))
            event_data['pupd_date'] = datetime.datetime.now()
            event_serializer = EventSerializer(event, data=event_data)
            if event_serializer.is_valid():
                event_serializer.save()
                return JsonResponse(event_serializer.data)
            return JsonResponse(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'Current user doesn\'t have privileges': current_user.id}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

@api_view(['GET'])
def event_detail_category(request, category):

    if request.method == 'GET':
        event = StreetEvent.objects.filter(category=category)
        event_serializer = EventSerializer(event, many=True)
        return JsonResponse(event_serializer.data, safe=False)

@api_view(['GET'])
def event_detail_distance(request, address, km):
    # find tutorial by pk (id)
    # GET / PUT
    if request.method == 'GET':
        eventList = StreetEvent.objects.all()
        geolocator = Nominatim(user_agent='street_event')

        data = list()
        event_serializer = EventSerializer(eventList.objects.all(), many=True)
        event = JsonResponse(event_serializer.data, safe=False)
        return JsonResponse(event)
        location = geolocator.geocode(str(address))
        geod = pyproj.Geod(ellps='WGS84')
        for ev in event:
            coord = ev['location'][1:-1].split(' ')
            angle1, angle2, distance = geod.inv(coord[0], coord[1], location.latitude, location.longitude)
            if distance <= km:
                data.append(ev)
        return JsonResponse(data, safe=False)
    return JsonResponse({'message': 'The Event does not exist'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def event_list_published(request):
    # GET all published tutorials
    event = StreetEvent.objects.filter(state='por validar')

    if request.method == 'GET':
        tutorials_serializer = EventSerializer(event, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)

@api_view(['GET', 'POST'])
def event_list(request):
    if request.method == 'GET':
        event = StreetEvent.objects.all()

        title = request.GET.get('title', None)
        if title is not None:
            event = event.filter(title__icontains=title)

        event_serializer = EventSerializer(event, many=True)
        return JsonResponse(event_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        geolocator = Nominatim(user_agent='street_event')
        event_data = JSONParser().parse(request)

        #Nao acha o autor?
        #event_data['author'] = request.user.id

        location = geolocator.geocode(str(event_data['address']))
        event_data['state'] = 'por validar'
        event_data['location'] = 'POINT({0} {1})'.format(location.latitude, location.longitude)
        event_data['pub_date'] = datetime.datetime.now()
        event_data['upd_date'] = datetime.datetime.now()
        event_serializer = EventSerializer(data=event_data)
        if event_serializer.is_valid():
            event_serializer.save()
            return JsonResponse(event_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)