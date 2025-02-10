from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from django.db.models import Sum
from core.permissions import IsTeamMember
from part.models import PartChoices
from teams.models import TeamChoices
from aircraft.models import Aircraft
from .models import Part, Inventory, Assembly, AssemblyPartUsage
from .serializers import (
    PartSerializer,
    InventorySerializer,
    AssemblySerializer,
)


class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeamMember]

    def get_queryset(self):
        """
        Kullanıcı sadece kendi takımının ürettiği parçaları görebilir.
        Montaj takımı (Assembly) tüm parçaları görebilir.
        """
        user = self.request.user
        if user.is_staff or user.team.name == TeamChoices.ASSEMBLY:
            return Part.objects.all()
        return Part.objects.filter(team=user.team)

    def perform_create(self, serializer):
        """
        Kullanıcının yalnızca kendi takımına ait parçaları üretmesini sağlar.
        Üretilen parça envantere eklenir.
        """
        user = self.request.user

        if not user.team:
            raise ValidationError({"error": "Bir takıma atanmış olmalısınız!"})

        part_name = serializer.validated_data["name"]
        team_id = user.team.name

        allowed_parts = {
            TeamChoices.WING: [PartChoices.WING],
            TeamChoices.FUSELAGE: [PartChoices.FUSELAGE],
            TeamChoices.TAIL: [PartChoices.TAIL],
            TeamChoices.AVIONICS: [PartChoices.AVIONICS],
        }
        if (
            team_id not in allowed_parts
            or part_name not in allowed_parts[team_id]
        ):
            raise ValidationError(
                {
                    "error": f"{TeamChoices(team_id).label} {PartChoices(part_name).label} üretemez!"
                }
            )

        part = serializer.save(team=user.team)

        inventory, created = Inventory.objects.get_or_create(
            part=part, defaults={"quantity": 1}
        )
        if not created:
            inventory.quantity += 1
            inventory.save()

    def perform_update(self, serializer):
        """
        Kullanıcı yalnızca kendi takımına ait parçaları güncelleyebilir.
        """
        user = self.request.user
        instance = self.get_object()

        if instance.team != user.team and not user.is_staff:
            raise ValidationError(
                {
                    "error": "Yalnızca kendi takımınıza ait parçaları güncelleyebilirsiniz!"
                }
            )

        serializer.save()

    def perform_destroy(self, instance):
        """
        Kullanıcı yalnızca kendi takımına ait parçaları silebilir (geri dönüşüme gönderebilir).
        """
        user = self.request.user

        if instance.team != user.team and not user.is_staff:
            raise ValidationError(
                {
                    "error": "Yalnızca kendi takımınıza ait parçaları silebilirsiniz!"
                }
            )

        Inventory.objects.filter(part=instance).delete()

        instance.delete()


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        Tüm envanterdeki parçaları listeleyen özel bir endpoint.
        """
        inventory_items = Inventory.objects.all()
        serializer = self.get_serializer(inventory_items, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def missing_parts(self, request):
        """
        Eksik parçaları kontrol eden özel bir endpoint.
        """
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

        return Response({"missing_parts": missing})


class AssemblyViewSet(viewsets.ModelViewSet):
    queryset = Assembly.objects.all()
    serializer_class = AssemblySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Montaj takımı ve admin üretilen uçakları görebilir.
        """
        user = self.request.user
        if user.is_staff or user.team.name == TeamChoices.ASSEMBLY:
            return Assembly.objects.all()
        return Assembly.objects.none()

    @action(detail=False, methods=["post"])
    def assemble(self, request):
        """
        Montaj takımı, envanterdeki parçaları kullanarak uçak üretir.
        Eğer eksik parça varsa, montaj başarısız olur.
        """
        user = request.user
        if user.team.name != TeamChoices.ASSEMBLY:
            return Response(
                {"error": "Sadece Montaj Takımı uçak üretebilir!"},
                status=status.HTTP_403_FORBIDDEN,
            )

        aircraft_id = request.data.get("aircraft")
        try:
            aircraft = Aircraft.objects.get(id=aircraft_id)
        except Aircraft.DoesNotExist:
            return Response(
                {"error": "Geçersiz uçak!"}, status=status.HTTP_400_BAD_REQUEST
            )

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

            print(
                f"Envanterde: {total_available} adet, Gerekli: {required_quantity}"
            )

            if total_available < required_quantity:
                missing_parts.append(
                    f"{PartChoices(part_id).label} ({required_quantity - total_available} eksik)"
                )

        if missing_parts:
            print("\nMontaj başarısız! Eksik parçalar:")
            for missing in missing_parts:
                print(f"   - {missing}")

            return Response(
                {"error": f"Eksik parçalar: {', '.join(missing_parts)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        print("\nTüm parçalar mevcut, montaj başlıyor...")
        assembly = Assembly.objects.create(aircraft=aircraft)
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
            print(
                "\nMontaj sırasında hata oldu! Kullanılan parçalar kaydedilemedi."
            )
            return Response(
                {"error": "Montaj sırasında parçalar kaydedilemedi!"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        print("\nMontaj tamamlandı! Yeni uçak üretildi.")
        return Response(
            AssemblySerializer(assembly).data, status=status.HTTP_201_CREATED
        )
