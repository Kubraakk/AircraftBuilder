from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.teams.models import Team
from apps.aircraft.models import Aircraft
from apps.part.models import Part
from core.enums import PartChoices, TeamChoices, AircraftChoices

User = get_user_model()


class CreatePartTestCase(APITestCase):

    def setUp(self):
        self.team = Team.objects.create(name=TeamChoices.AVIONICS)
        self.aircraft = Aircraft.objects.create(
            aircraft_name=AircraftChoices.TB2
        )

        self.user = User.objects.create_user(
            email="testuser@example.com",
            first_name="Test",
            last_name="User",
            password="testpassword",
            team=self.team,
        )

        self.client.force_authenticate(user=self.user)

        self.part_data = {
            "name": PartChoices.AVIONICS.value,
            "aircraft": self.aircraft.id,
            "team": self.team.id,
        }

    def test_create_part_success(self):
        response = self.client.post(
            "/api/parts/parts/", self.part_data, format="json"
        )

        if response.status_code != status.HTTP_201_CREATED:
            print("Hata:", response.json())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Part.objects.filter(name=self.part_data["name"]).exists()
        )

    def test_create_part_unauthorized(self):
        self.client.logout()
        response = self.client.post(
            "/api/parts/parts/", self.part_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
