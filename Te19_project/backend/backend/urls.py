"""backend URL Configuration
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView
from api import views as api_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # API
    path('api/insights/vehicle-growth', api_views.vehicle_growth, name='vehicle_growth'),
    path('api/insights/cbd-population', api_views.cbd_population, name='cbd_population'),
    path('api/parking/', include('parking.urls')),

    # to frontend index.html ---
    re_path(r'^(?!api/).*$', TemplateView.as_view(template_name='index.html')),
]
