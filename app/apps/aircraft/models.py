from django.db import models
from core.enums import AircraftChoices
from core.mixins import AuditMixin
from django.utils.translation import gettext_lazy as _


class Aircraft(AuditMixin):
    aircraft_name = models.IntegerField(  # enum used for aircraft name
        choices=AircraftChoices.choices, unique=True
    )

    class Meta:
        verbose_name = _("Aircraft")
        verbose_name_plural = _("Aircrafts")

    def __str__(self):
        return self.get_aircraft_name_display()
