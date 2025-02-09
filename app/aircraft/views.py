from rest_framework import viewsets
from .models import Aircraft
from .serializers import AircraftSerializer
from rest_framework.permissions import IsAuthenticated


class AircraftViewSet(viewsets.ModelViewSet):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer
    permission_classes = [IsAuthenticated]
