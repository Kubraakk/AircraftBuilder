"""
Models for aircraft
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class AircraftChoices(models.IntegerChoices):
    TB2 = 1, "Bayraktar TB2"
    TB3 = 2, "Bayraktar TB3"
    AKINCI = 3, "Akıncı"
    KIZILELMA = 4, "Kızılelma"


class Aircraft(models.Model):
    aircraft_name = models.IntegerField(
        choices=AircraftChoices.choices, unique=True
    )

    class Meta:
        verbose_name = _("Aircraft")
        verbose_name_plural = _("Aircrafts")

    def __str__(self):
        return self.get_aircraft_name_display()
