from apps.aircraft.models import Aircraft
from core.services.base_service import BaseService


class AircraftService(BaseService):
    """Service class for managing aircraft"""

    def __init__(self):
        super().__init__(Aircraft)
