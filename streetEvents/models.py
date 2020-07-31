from django.db import models
from model_utils import Choices

# Create your models here.
class StreetEvent(models.Model):
    stateChoices = Choices(
        ('por validar', ('por validar')),
        ('validado',  ('validado')),
        ('Resolvido', ('Resolvido'))
    )

    categoryChoices = Choices(
        ('CONSTRUCTION', ('CONSTRUCTION')),
        ('SPECIAL_EVENT', ('SPECIAL_EVENT')),
        ('INCIDENT', ('INCIDENT')),
        ('WEATHER_CONDITION', ('WEATHER_CONDITION')),
        ('ROAD_CONDITION', ('ROAD_CONDITION'))
    )

    author = models.CharField(max_length=200)
    description = models.CharField(max_length=600)
    address = models.CharField(max_length=600)
    location = models.CharField(max_length=200, default='POINT(0 0)')
    state = models.CharField(max_length=50, choices=stateChoices)
    category = models.CharField(max_length=50, choices=categoryChoices)
    pub_date = models.DateTimeField('date published')
    upd_date = models.DateTimeField('date upated')

    def __unicode__(self):
        return self.category
        return '{:15s} : {:20s} : {:30s}'.format(self.state, self.category, self.description)
