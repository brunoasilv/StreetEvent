from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from .models import Occurrence, OccurrenceState, OccurrenceCategory
from datetime import datetime, date
import geocoder
from geopy.geocoders import Nominatim

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser

ocState = ['por validar', 'validado', 'resolvido']
ocCategory = ['CONSTRUCTION', 'SPECIAL_EVENT', 'INCIDENT', 'WEATHER_CONDITION', 'ROAD_CONDITION']

# Create your views here.
def index(request):
    return render(request, 'events/index.html')

def createOccurrence(request):
    #oc = get_object_or_404(Occurrence)
    return render(request, 'events/createOccurrence.html', {})

def registerOccurrence(request):
    geolocator = Nominatim(user_agent='street_event')

    try:
        oc = Occurrence()
        occurrence = dict()
        occurrence['description'] = request.POST.get('description')
        loc =request.POST.get('address')
        location = geolocator.geocode(str(loc))
        occurrence['location'] = 'POINT({0} {1})'.format(location.latitude, location.longitude)
        occurrence['occurrenceCategory'] = request.POST.get('occurrenceCategory')
        occurrence['occurrenceState'] = request.POST.get('occurrenceState')
        occurrence['author'] = 'todo'#request.POST.get('')
        occurrence['createDate'] = datetime.now()
        occurrence['updateDate'] = datetime.now()
        oc = Occurrence(id=Occurrence.objects.count()+1, author=occurrence['author'], description=occurrence['description'], location=occurrence['location'], state=occurrence['occurrenceState'], category=occurrence['occurrenceCategory'], pub_date=occurrence['createDate'], upd_date=occurrence['updateDate'])
        oc.save()
        return HttpResponse("Inserted SuccessFuly...")
    except Exception as e:
        # Redisplay the question voting form.
        return render(request, 'events/createOccurrence.html', {
            'error_message': request.POST,
            'error_message': "Missing field.",
        })


