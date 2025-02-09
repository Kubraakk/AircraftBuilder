from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
import uuid
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Custom user manager where email is the unique identifier"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model using email for authentication"""

    uuid = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False, primary_key=True
    )
    email = models.EmailField(max_length=255, unique=True, blank=False)
    username = models.CharField(max_length=255)
    team = models.ForeignKey(
        "teams.Team", on_delete=models.SET_NULL, null=True, blank=True
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("Personal")
        verbose_name_plural = _("Personals")

    def __str__(self):
        return f"{self.username} ({self.email})"
