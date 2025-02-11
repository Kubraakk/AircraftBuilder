"""
Serializers for the user API View
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers
from apps.user.services import UserService

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user object (Read & Update)"""

    class Meta:
        model = User
        fields = ["uuid", "email", "first_name", "last_name", "team"]
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 5,
                "style": {"input_type": "password"},
            }
        }


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""

    password = serializers.CharField(
        write_only=True, min_length=5, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password", "team")

    def create(self, validated_data):
        """Use UserService to create a user"""
        user_service = UserService()
        return user_service.create_user(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            password=validated_data["password"],
            team=validated_data.get("team"),
        )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )

    def validate(self, data):
        """Use UserService to authenticate user"""
        user_service = UserService()
        return user_service.authenticate_user(
            data.get("email"), data.get("password")
        )
