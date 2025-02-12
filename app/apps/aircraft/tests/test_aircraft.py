from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.teams.models import Team
from apps.aircraft.models import Aircraft
from apps.part.models import Part, Inventory, Assembly
from core.enums import PartChoices, TeamChoices, AircraftChoices

User = get_user_model()


class AssembleAircraftTestCase(APITestCase):

    def setUp(self):
        self.assembly_team = Team.objects.create(name=TeamChoices.ASSEMBLY)
        self.other_team = Team.objects.create(name=TeamChoices.WING)

        self.assembly_user = User.objects.create_user(
            email="assembly@example.com",
            first_name="Montaj",
            last_name="User",
            password="testpassword",
            team=self.assembly_team,
        )

        self.other_user = User.objects.create_user(
            email="wing@example.com",
            first_name="Wing",
            last_name="User",
            password="testpassword",
            team=self.other_team,
        )

        self.aircraft = Aircraft.objects.create(
            aircraft_name=AircraftChoices.TB2.value
        )

        self.parts = []
        for part_choice in [
            PartChoices.WING,
            PartChoices.FUSELAGE,
            PartChoices.TAIL,
            PartChoices.AVIONICS,
        ]:
            part = Part.objects.create(
                name=part_choice.value,
                aircraft=self.aircraft,
                team=self.assembly_team,
            )
            self.parts.append(part)
            Inventory.objects.create(part=part, quantity=2)

        self.client.force_authenticate(user=self.assembly_user)

    def test_assemble_aircraft_success(self):
        response = self.client.post(
            "/api/parts/assembly/assemble/",
            {"aircraft": self.aircraft.id},
            format="json",
        )

        if response.status_code != status.HTTP_201_CREATED:
            print("Hata:", response.json())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Assembly.objects.filter(aircraft=self.aircraft).exists()
        )

    def test_assemble_aircraft_missing_parts(self):
        Inventory.objects.all().delete()

        response = self.client.post(
            "/api/parts/assembly/assemble/",
            {"aircraft": self.aircraft.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.json())

    def test_assemble_aircraft_wrong_team(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.post(
            "/api/parts/assembly/assemble/",
            {"aircraft": self.aircraft.id},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("error", response.json())

    def test_assemble_aircraft_unauthenticated(self):
        self.client.logout()

        response = self.client.post(
            "/api/parts/assembly/assemble/",
            {"aircraft": self.aircraft.id},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
