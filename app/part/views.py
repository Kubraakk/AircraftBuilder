from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum
from .models import Part, Inventory, Assembly, AssemblyPartUsage
from rest_framework import serializers
from .serializers import (
    PartSerializer,
    InventorySerializer,
    AssemblySerializer,
)


class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Kullanıcının takımına ait parçaları döndür.
        """
        user = self.request.user
        return Part.objects.filter(team=user.team)

    def perform_create(self, serializer):
        """
        Takımlar yalnızca kendi üretebilecekleri parçaları oluşturabilir.
        """
        user = self.request.user
        if user.team is None:
            return Response(
                {"error": "Bir takıma atanmış olmalısınız!"}, status=400
            )

        serializer.save(team=user.team)


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticated]

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
                        "part": part.name,
                        "aircraft": part.aircraft.get_aircraft_name_display(),
                    }
                )

        return Response({"missing_parts": missing})


class AssemblyViewSet(viewsets.ModelViewSet):
    queryset = Assembly.objects.all()
    serializer_class = AssemblySerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Montaj işlemi sırasında eksik parça olup olmadığını kontrol eder.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)

    def perform_create(self, serializer):
        """
        Montaj işlemi gerçekleştiğinde stoklardan düşülmeli.
        """
        assembly = serializer.save()
        parts_usage = serializer.validated_data["parts_used"]

        for part_usage in parts_usage:
            part = part_usage["part"]
            quantity_used = part_usage["quantity_used"]

            inventory_item = Inventory.objects.get(part=part)
            if inventory_item.quantity < quantity_used:
                raise serializers.ValidationError(
                    f"{part.name} için yeterli stok yok!"
                )

            inventory_item.quantity -= quantity_used
            inventory_item.save()

            AssemblyPartUsage.objects.create(
                assembly=assembly, part=part, quantity_used=quantity_used
            )
