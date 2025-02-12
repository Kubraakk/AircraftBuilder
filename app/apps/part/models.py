from django.db import models
from apps.aircraft.models import Aircraft
from apps.teams.models import Team
from core.enums import PartChoices
from core.mixins import AuditMixin
from django.utils.translation import gettext_lazy as _


class Part(AuditMixin):
    name = models.IntegerField(choices=PartChoices.choices)
    aircraft = models.ForeignKey(
        Aircraft, on_delete=models.CASCADE, related_name="parts"
    )
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="produced_parts"
    )

    class Meta:
        verbose_name = _("Part")
        verbose_name_plural = _("Parts")

    def __str__(self):
        return f"{self.get_name_display()} for {self.aircraft.get_aircraft_name_display()}"


class Inventory(AuditMixin):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _("Inventory")
        verbose_name_plural = _("Inventories")

    def __str__(self):
        return f"{self.part.get_name_display()} - {self.quantity} adet"


class Assembly(AuditMixin):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    parts_used = models.ManyToManyField(Part, through="AssemblyPartUsage")

    class Meta:
        verbose_name = _("Assembly")
        verbose_name_plural = _("Assemblies")

    def __str__(self):
        return f"{self.aircraft.get_aircraft_name_display()} Montajı"


class AssemblyPartUsage(AuditMixin):
    assembly = models.ForeignKey(Assembly, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity_used = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity_used}x {self.part.get_name_display()} in {self.assembly.aircraft.get_aircraft_name_display()}"
