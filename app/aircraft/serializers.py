from rest_framework import serializers
from .models import Aircraft


class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ["id", "aircraft_name"]
