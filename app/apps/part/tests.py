from django.test import TestCase
from apps.part.models import Part, Inventory
from apps.part.services import PartService
from apps.teams.models import Team
from apps.aircraft.models import Aircraft
from core.enums import PartChoices, TeamChoices


class PartServiceTest(TestCase):
    """Unit tests for PartService"""

    def setUp(self):
        self.service = PartService()

        # Create teams and aircraft
        self.team_wing = Team.objects.create(name=TeamChoices.WING)
        self.team_fuselage = Team.objects.create(name=TeamChoices.FUSELAGE)
        self.aircraft = Aircraft.objects.create(name="TB2")

    def test_create_part_success(self):
        """Should successfully create a part and add it to inventory"""
        part = self.service.create_part(
            name=PartChoices.WING, aircraft=self.aircraft, team=self.team_wing
        )

        # Validate that part and inventory were created
        self.assertEqual(Part.objects.count(), 1)
        self.assertEqual(Inventory.objects.count(), 1)

        inventory = Inventory.objects.get(part=part)
        self.assertEqual(inventory.quantity, 1)

    def test_create_part_wrong_team(self):
        """Should raise an error if a team tries to create an unauthorized part"""
        with self.assertRaises(Exception):
            self.service.create_part(
                name=PartChoices.WING,
                aircraft=self.aircraft,
                team=self.team_fuselage,
            )

        self.assertEqual(Part.objects.count(), 0)
        self.assertEqual(Inventory.objects.count(), 0)

    def test_get_parts_for_team(self):
        """Should retrieve only the parts belonging to the specified team"""
        self.service.create_part(
            name=PartChoices.WING, aircraft=self.aircraft, team=self.team_wing
        )
        self.service.create_part(
            name=PartChoices.WING, aircraft=self.aircraft, team=self.team_wing
        )

        parts = self.service.get_parts_for_team(self.team_wing)
        self.assertEqual(parts.count(), 2)

        parts_other_team = self.service.get_parts_for_team(self.team_fuselage)
        self.assertEqual(parts_other_team.count(), 0)

    def test_delete_part(self):
        """Should delete a part and remove it from inventory"""
        part = self.service.create_part(
            name=PartChoices.WING, aircraft=self.aircraft, team=self.team_wing
        )
        self.service.delete_part(part)

        self.assertEqual(Part.objects.count(), 0)
        self.assertEqual(Inventory.objects.count(), 0)
