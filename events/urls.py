from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('createOccurrence/', views.createOccurrence, name='createOccurrence'),
    path('createOccurrence/register', views.registerOccurrence, name='registerOccurrence'),
]