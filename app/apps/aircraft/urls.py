from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.aircraft.views import AircraftViewSet

router = DefaultRouter()
router.register(r"", AircraftViewSet, basename="aircraft")

urlpatterns = [
    path("", include(router.urls)),
]
