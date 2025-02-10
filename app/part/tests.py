from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from user.models import User
from teams.models import Team
from .models import Part, Inventory
from aircraft.models import Aircraft


class PartTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(name="Wing")
        self.user = User.objects.create_user(
            email="test@company.com",
            password="password123",
            first_name="Test",
            last_name="User",
            team=self.team,
        )
        self.aircraft = Aircraft.objects.create(aircraft_name=1)  # TB2

        self.client.force_authenticate(user=self.user)

    def test_create_part(self):
        """Kullanıcı sadece kendi takımına ait parça üretebilir mi?"""
        payload = {
            "name": "Wing",
            "aircraft": self.aircraft.id,
            "team": self.team.id,
        }
        response = self.client.post("/api/parts/", payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Wing")

    def test_forbidden_part_creation(self):
        """Kullanıcı başka takım için parça üretemez mi?"""
        other_team = Team.objects.create(name="Tail")
        payload = {
            "name": "Tail",
            "aircraft": self.aircraft.id,
            "team": other_team.id,
        }
        response = self.client.post("/api/parts/", payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class InventoryTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(name="Wing")
        self.user = User.objects.create_user(
            email="test@company.com", password="password123", team=self.team
        )
        self.aircraft = Aircraft.objects.create(aircraft_name=1)  # TB2
        self.part = Part.objects.create(
            name="Wing", aircraft=self.aircraft, team=self.team
        )
        self.inventory = Inventory.objects.create(part=self.part, quantity=10)

        self.client.force_authenticate(user=self.user)

    def test_inventory_list(self):
        """Envanter listesi çekilebiliyor mu?"""
        response = self.client.get("/api/inventory/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_inventory_stock_update(self):
        """Admin stok ekleyip çıkarabiliyor mu?"""
        self.user.is_staff = True
        self.user.save()

        payload = {"action": "increase", "amount": 5}
        response = self.client.post(
            f"/api/inventory/{self.inventory.id}/update_stock/", payload
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.quantity, 15)


class AssemblyTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(name="Assembly")
        self.user = User.objects.create_user(
            email="montaj@company.com", password="password123", team=self.team
        )
        self.aircraft = Aircraft.objects.create(aircraft_name=1)
        self.part = Part.objects.create(
            name="Wing", aircraft=self.aircraft, team=self.team
        )
        self.inventory = Inventory.objects.create(part=self.part, quantity=5)

        self.client.force_authenticate(user=self.user)

    def test_assembly_process(self):
        """Montaj işlemi başarılı şekilde yapılabiliyor mu?"""
        payload = {
            "aircraft": self.aircraft.id,
            "parts_used": [{"part": self.part.id, "quantity_used": 1}],
        }
        response = self.client.post("/api/assembly/", payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.quantity, 4)
