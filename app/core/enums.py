"""
Enum definitions for the application.
"""

from django.db import models


class TeamChoices(models.IntegerChoices):
    """
    Enum for team choices.

    Attributes:
        WING (int): Represents the Wing Team.
        FUSELAGE (int): Represents the Fuselage Team.
        TAIL (int): Represents the Tail Team.
        AVIONICS (int): Represents the Avionics Team.
        ASSEMBLY (int): Represents the Assembly Team.
    """

    WING = 1, "Kanat Takımı"
    FUSELAGE = 2, "Gövde Takımı"
    TAIL = 3, "Kuyruk Takımı"
    AVIONICS = 4, "Aviyonik Takımı"
    ASSEMBLY = 5, "Montaj Takımı"


class AircraftChoices(models.IntegerChoices):
    """
    Enum for aircraft models.

    Attributes:
        TB2 (int): Represents the Bayraktar TB2 model.
        TB3 (int): Represents the Bayraktar TB3 model.
        AKINCI (int): Represents the Akıncı model.
        KIZILELMA (int): Represents the Kızılelma model.
    """

    TB2 = 1, "Bayraktar TB2"
    TB3 = 2, "Bayraktar TB3"
    AKINCI = 3, "Akıncı"
    KIZILELMA = 4, "Kızılelma"


class PartChoices(models.IntegerChoices):
    """
    Enum for aircraft parts.

    Attributes:
        WING (int): Represents the Wing part.
        FUSELAGE (int): Represents the Fuselage part.
        TAIL (int): Represents the Tail part.
        AVIONICS (int): Represents the Avionics part.
    """

    WING = 1, "Kanat"
    FUSELAGE = 2, "Gövde"
    TAIL = 3, "Kuyruk"
    AVIONICS = 4, "Aviyonik"
