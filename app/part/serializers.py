from rest_framework import serializers
from .models import Part, Inventory, Assembly, AssemblyPartUsage


# 1️⃣ Parça Serializer
class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = ["id", "name", "aircraft", "team"]


# 2️⃣ Envanter Serializer
class InventorySerializer(serializers.ModelSerializer):
    part_name = serializers.ReadOnlyField(source="part.name")
    aircraft_name = serializers.ReadOnlyField(source="part.aircraft.name")

    class Meta:
        model = Inventory
        fields = ["id", "part_name", "aircraft_name", "quantity"]


# 3️⃣ Montaj Serializer
class AssemblyPartUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssemblyPartUsage
        fields = ["part", "quantity_used"]


class AssemblySerializer(serializers.ModelSerializer):
    parts_used = AssemblyPartUsageSerializer(many=True)

    class Meta:
        model = Assembly
        fields = ["id", "aircraft", "parts_used", "created_at"]

    def validate(self, data):
        """
        Uçak üretimi sırasında envanterde eksik parça olup olmadığını kontrol eder.
        """
        aircraft = data["aircraft"]
        required_parts = aircraft.parts.all()
        inventory = Inventory.objects.filter(part__aircraft=aircraft)

        missing_parts = []
        for part in required_parts:
            available = inventory.filter(part=part).first()
            if not available or available.quantity < 1:
                missing_parts.append(part.name)

        if missing_parts:
            raise serializers.ValidationError(
                f"Eksik parçalar: {', '.join(missing_parts)}"
            )

        return data

    def create(self, validated_data):
        """
        Montaj işlemi gerçekleştiğinde, kullanılan parçalar envanterden düşülmelidir.
        """
        parts_data = validated_data.pop("parts_used")
        assembly = Assembly.objects.create(**validated_data)

        for part_usage in parts_data:
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

        return assembly
