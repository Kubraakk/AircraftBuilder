from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAdminOrReadOnly, IsTeamMember
from apps.teams.serializers import TeamSerializer
from apps.teams.services import TeamService


class TeamViewSet(viewsets.ModelViewSet):
    """Manage teams in the database using TeamService"""

    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly | IsTeamMember]
    team_service = TeamService()

    def get_queryset(self):
        """Retrieve all teams using TeamService"""
        return self.team_service.get_all_teams()

    def perform_create(self, serializer):
        """Create a new team using TeamService"""
        team_name = serializer.validated_data.get("name")
        team = self.team_service.create_team(name=team_name)
        serializer.instance = team
