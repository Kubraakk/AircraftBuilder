from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.user.serializers import (
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class UserView(APIView):
    """
    API endpoint to retrieve authenticated user details.

    This view requires authentication and returns the current user's details.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class RegisterView(CreateAPIView):
    """
    API endpoint for user registration.

    This view allows new users to register by providing required credentials.
    """

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LoginView(APIView):
    """
    API endpoint for user authentication.

    This view authenticates users and returns JWT access and refresh tokens.
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        """Authenticate user and return JWT tokens"""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
