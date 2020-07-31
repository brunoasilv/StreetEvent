from rest_framework import serializers
from streetEvents.models import StreetEvent

class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = StreetEvent
        fields = ('id',
                  'author',
                  'description',
                  'address',
                  'location',
                  'state',
                  'category',
                  'pub_date',
                  'upd_date'
                  )