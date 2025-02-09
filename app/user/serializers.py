"""
Serializers for the user API View
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = User
        fields = ["email", "username", "team", "password"]
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 5,
                "style": {"input_type": "password"},
            }
        }

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        user = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
            team=validated_data.get("team"),
        )
        return user


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""

    password = serializers.CharField(
        write_only=True, min_length=5, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ("email", "username", "password", "team")

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
            team=validated_data.get("team"),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
