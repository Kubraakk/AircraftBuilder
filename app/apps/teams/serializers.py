from rest_framework import serializers
from apps.teams.models import Team


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for the team model"""

    class Meta:
        model = Team
        fields = ["id", "name"]
