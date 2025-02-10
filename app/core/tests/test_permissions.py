from user.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class PermissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="user@company.com", password="password123"
        )
        self.admin = User.objects.create_superuser(
            email="admin@company.com", password="admin123"
        )

    def test_admin_can_edit_inventory(self):
        """Admin stok güncelleyebilir mi?"""
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch("/api/inventory/1/", {"quantity": 50})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_edit_inventory(self):
        """Normal kullanıcı stok güncelleyemez mi?"""
        self.client.force_authenticate(user=self.user)
        response = self.client.patch("/api/inventory/1/", {"quantity": 50})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
