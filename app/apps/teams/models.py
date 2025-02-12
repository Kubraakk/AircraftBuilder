from django.db import models
from django.utils.translation import gettext_lazy as _
from core.enums import TeamChoices
from core.mixins import AuditMixin


class Team(AuditMixin):
    """Represents a production team"""

    name = models.IntegerField(choices=TeamChoices.choices, unique=True)

    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")

    def __str__(self):
        return self.get_name_display()
