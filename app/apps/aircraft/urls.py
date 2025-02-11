from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.aircraft.views import AircraftViewSet, AircraftCountView

router = DefaultRouter()
router.register(r"", AircraftViewSet, basename="aircraft")

urlpatterns = [
    path("", include(router.urls)),
    path("count/", AircraftCountView.as_view(), name="aircraft-count"),
]
