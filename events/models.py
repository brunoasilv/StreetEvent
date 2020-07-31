from django.db import models

class OccurrenceCategory(models.Model):
    category = models.CharField(primary_key=True, max_length=80, default='')
    def __str__(self):
        return self.category

class OccurrenceState(models.Model):
    state = models.CharField(primary_key=True, max_length=50, default='')
    def __str__(self):
        return self.state

class Occurrence(models.Model):
    id = models.CharField(primary_key=True, max_length=200)
    author = models.CharField(max_length=200)
    description = models.CharField(max_length=600)
    location = models.CharField(max_length=200, default='POINT(0 0)')
    state = models.CharField(max_length=200, default='por validar')
    category = models.CharField(max_length=200, default='CONSTRUCTION')
    pub_date = models.DateTimeField('date published')
    upd_date = models.DateTimeField('date upated')
    #g = geocoder.google(models.CharField(max_length=200))
    #geo_location = 'POINT({s} {s})'.format(str(g.latlng[0]), str(g.latlng[1]))
