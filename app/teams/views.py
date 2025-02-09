from rest_framework import viewsets
from .models import Team
from .serializers import TeamSerializer
from rest_framework.permissions import IsAuthenticated


class TeamViewSet(viewsets.ModelViewSet):
    """Manage teams in the database"""

    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]
