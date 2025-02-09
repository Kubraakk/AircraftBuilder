from django.db import models
from django.utils.translation import gettext_lazy as _


class TeamChoices(models.IntegerChoices):
    WING = 1, "Kanat Takımı"
    FUSELAGE = 2, "Gövde Takımı"
    TAIL = 3, "Kuyruk Takımı"
    AVIONICS = 4, "Aviyonik Takımı"
    ASSEMBLY = 5, "Montaj Takımı"


class Team(models.Model):
    """Represents a production team"""

    name = models.IntegerField(choices=TeamChoices.choices, unique=True)

    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")

    def __str__(self):
        return self.get_name_display()
