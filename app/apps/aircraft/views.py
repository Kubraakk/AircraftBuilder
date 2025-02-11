from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAdminOrReadOnly
from apps.aircraft.serializers import AircraftSerializer
from apps.aircraft.services import AircraftService


class AircraftViewSet(viewsets.ModelViewSet):
    """Manage aircraft in the database"""

    serializer_class = AircraftSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    service = AircraftService()

    def get_queryset(self):
        """Retrieve all aircrafts"""
        return self.service.get_all()
