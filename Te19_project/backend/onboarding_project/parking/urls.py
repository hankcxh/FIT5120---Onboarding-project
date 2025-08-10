
from django.urls import path
from . import views
from parking.views import zones_in_bbox
urlpatterns = [
    path('', views.parking_map, name='parking_map'),          # homepage -map
    path('api/zones', views.zones_in_bbox, name='zones_in_bbox'),
    path('api/status', views.status, name='status'), # JSON API for map markers
]
