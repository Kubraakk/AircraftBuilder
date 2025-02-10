"""
Serializers for the user API View
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

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

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        user = User.objects.create_user(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
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
        fields = ("email", "first_name", "last_name", "password", "team")

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        user = User(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            team=validated_data.get("team"),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError(
                "No active account found with the given credentials"
            )

        if not user.is_active:
            raise serializers.ValidationError("User is inactive")

        return {"user": user}
