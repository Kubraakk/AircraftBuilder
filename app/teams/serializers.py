from rest_framework import serializers
from .models import Team


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for the team model"""

    class Meta:
        model = Team
        fields = ["id", "name"]
