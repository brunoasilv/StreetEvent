from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list),
    path('help', views.event_comands_list),
    path('id=<int:id>', views.event_detail_id),
    path('category=<category>', views.event_detail_category),
    path('address=<address>&km=<int:km>', views.event_detail_distance),
    path('published', views.event_list_published),
]