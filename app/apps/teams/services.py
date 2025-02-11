from apps.teams.models import Team
from core.services.base_service import BaseService


class TeamService(BaseService):
    """Service class for managing teams"""

    def __init__(self):
        super().__init__(Team)

    def create_team(self, name):
        """Create a new team"""
        return self.create(name=name)
