from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import vessel_dashboard, get_vessel_readings

urlpatterns = [
    path('', vessel_dashboard, name='vessel_dashboard'),
    path('get_vessel_readings/', get_vessel_readings, name='get_vessel_readings'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
