from rest_framework import serializers
from apps.aircraft.models import Aircraft


class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ["id", "aircraft_name"]
