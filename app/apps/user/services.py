from core.services.base_service import BaseService
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError

User = get_user_model()


class UserService(BaseService):
    """
    Service class for handling user-related database operations.
    """

    def __init__(self):
        super().__init__(User)

    def create_user(self, email, first_name, last_name, password, team=None):
        """Create and return a user with encrypted password"""
        user = User.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            team=team,
        )
        user.set_password(password)
        user.save()
        return user

    def authenticate_user(self, email, password):
        """Authenticate a user and return JWT tokens"""
        user = authenticate(email=email, password=password)

        if not user:
            raise ValidationError(
                "No active account found with the given credentials"
            )

        if not user.is_active:
            raise ValidationError("User is inactive")

        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
