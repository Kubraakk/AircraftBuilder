"""
Views for the User API
"""

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
