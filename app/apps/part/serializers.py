from rest_framework import serializers
from collections import defaultdict
from apps.part.models import Part, Inventory, Assembly, AssemblyPartUsage


class PartSerializer(serializers.ModelSerializer):
    name_display = serializers.CharField(
        source="get_name_display", read_only=True
    )

    class Meta:
        model = Part
        fields = ["id", "name", "name_display", "aircraft", "team"]


class InventorySerializer(serializers.ModelSerializer):
    part_name = serializers.CharField(
        source="part.get_name_display", read_only=True
    )
    aircraft_name = serializers.CharField(
        source="part.aircraft.get_aircraft_name_display", read_only=True
    )

    class Meta:
        model = Inventory
        fields = ["id", "part_name", "aircraft_name", "quantity"]


class AssemblyPartUsageSerializer(serializers.ModelSerializer):
    part_name = serializers.CharField(source="part.get_name_display")

    class Meta:
        model = AssemblyPartUsage
        fields = ["part_name", "quantity_used"]


class AssemblySerializer(serializers.ModelSerializer):
    aircraft_name = serializers.CharField(
        source="aircraft.get_aircraft_name_display", read_only=True
    )
    parts_used = serializers.SerializerMethodField()

    class Meta:
        model = Assembly
        fields = [
            "id",
            "aircraft",
            "aircraft_name",
            "parts_used",
            "created_at",
        ]

    def get_parts_used(self, obj):
        """
        Listing of the parts used in assembly.
        """
        part_usage_dict = defaultdict(int)

        for usage in AssemblyPartUsage.objects.filter(assembly=obj):
            part_usage_dict[
                usage.part.get_name_display()
            ] += usage.quantity_used

        return [
            {"part_name": part, "quantity_used": quantity}
            for part, quantity in part_usage_dict.items()
        ]
