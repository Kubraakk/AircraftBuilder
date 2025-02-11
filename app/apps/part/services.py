from django.db.models import Sum
from core.services.base_service import BaseService
from apps.part.models import Part, Inventory, Assembly, AssemblyPartUsage
from apps.teams.models import TeamChoices
from apps.part.models import PartChoices
from rest_framework.exceptions import ValidationError


class PartService(BaseService):
    """Service class for managing parts"""

    def __init__(self):
        super().__init__(Part)

    def get_parts_for_team(self, team):
        """Takıma ait parçaları getir"""
        return self.get_all(team=team)

    def create_part(self, name, aircraft, team):
        """Sadece ilgili takımın üretebileceği parçaları üretmesine izin verir."""
        allowed_parts = {
            TeamChoices.WING: [PartChoices.WING],
            TeamChoices.FUSELAGE: [PartChoices.FUSELAGE],
            TeamChoices.TAIL: [PartChoices.TAIL],
            TeamChoices.AVIONICS: [PartChoices.AVIONICS],
        }

        if (
            team.name not in allowed_parts
            or name not in allowed_parts[team.name]
        ):
            raise ValidationError(
                {
                    "error": f"{TeamChoices(team.name).label} {PartChoices(name).label} üretemez!"
                }
            )

        # Parçayı oluştur
        part = self.create(name=name, aircraft=aircraft, team=team)

        # Envantere ekle
        inventory, created = Inventory.objects.get_or_create(
            part=part, defaults={"quantity": 1}
        )
        if not created:
            inventory.quantity += 1
            inventory.save()

        return part

    def delete_part(self, part):
        """Parçayı envanterden kaldır ve sil"""
        Inventory.objects.filter(part=part).delete()
        return part.delete()


class InventoryService(BaseService):
    """Service class for managing inventory"""

    def __init__(self):
        super().__init__(Inventory)

    def get_inventory(self):
        """Tüm envanteri getir"""
        return self.get_all()

    def get_missing_parts(self):
        """Eksik parçaları getir"""
        missing = []
        for part in Part.objects.all():
            inventory_item = Inventory.objects.filter(part=part).aggregate(
                Sum("quantity")
            )
            quantity = inventory_item["quantity__sum"] or 0
            if quantity == 0:
                missing.append(
                    {
                        "part": part.get_name_display(),
                        "aircraft": part.aircraft.get_aircraft_name_display(),
                        "team": part.team.get_name_display(),
                    }
                )
        return missing


class AssemblyService(BaseService):
    """Service class for managing assembly"""

    def __init__(self):
        super().__init__(Assembly)

    def assemble_aircraft(self, aircraft, user):
        """Montaj işlemini gerçekleştir, eksik parçaları kontrol et ve envanterden düş"""

        from core.enums import PartChoices, TeamChoices

        if user.team.name != TeamChoices.ASSEMBLY:
            return {"error": "Sadece Montaj Takımı uçak üretebilir!"}, 403

        required_parts = {
            PartChoices.WING: 2,
            PartChoices.FUSELAGE: 1,
            PartChoices.TAIL: 1,
            PartChoices.AVIONICS: 1,
        }

        missing_parts = []
        for part_id, required_quantity in required_parts.items():
            part = (
                Part.objects.filter(aircraft=aircraft, name=part_id)
                .order_by("-id")
                .first()
            )

            if not part:
                missing_parts.append(
                    f"{PartChoices(part_id).label} (hiç üretilmemiş!)"
                )
                continue

            inventory_items = Inventory.objects.filter(part=part)
            total_available = sum([item.quantity for item in inventory_items])

            if total_available < required_quantity:
                missing_parts.append(
                    f"{PartChoices(part_id).label} ({required_quantity - total_available} eksik)"
                )

        if missing_parts:
            return {
                "error": f"Eksik parçalar: {', '.join(missing_parts)}"
            }, 400

        assembly = self.create(aircraft=aircraft)
        used_parts = []

        for part_id, required_quantity in required_parts.items():
            part = (
                Part.objects.filter(aircraft=aircraft, name=part_id)
                .order_by("-id")
                .first()
            )
            inventory_items = Inventory.objects.filter(part=part).order_by(
                "id"
            )
            total_removed = 0

            for inventory in inventory_items:
                if total_removed >= required_quantity:
                    break

                to_remove = min(
                    required_quantity - total_removed, inventory.quantity
                )
                inventory.quantity -= to_remove
                total_removed += to_remove
                inventory.save()

            usage, created = AssemblyPartUsage.objects.get_or_create(
                assembly=assembly,
                part=part,
                defaults={"quantity_used": required_quantity},
            )
            if not created:
                usage.quantity_used += required_quantity
                usage.save()

            used_parts.append(usage)

        if not used_parts:
            return {"error": "Montaj sırasında parçalar kaydedilemedi!"}, 500

        return assembly, 201
