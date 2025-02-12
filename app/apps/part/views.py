from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from core.permissions import IsTeamMember
from core.enums import TeamChoices
from apps.aircraft.models import Aircraft
from apps.part.serializers import (
    PartSerializer,
    InventorySerializer,
    AssemblySerializer,
)
from apps.part.services import (
    PartService,
    InventoryService,
    AssemblyService,
)


class PartViewSet(viewsets.ModelViewSet):
    serializer_class = PartSerializer
    permission_classes = [IsAuthenticated, IsTeamMember]
    service = PartService()

    def get_queryset(self):
        """The user can only see the parts produced by her own team."""
        user = self.request.user
        if user.is_staff or user.team.name == TeamChoices.ASSEMBLY:
            return self.service.get_all()
        return self.service.get_parts_for_team(user.team)

    def perform_create(self, serializer):
        """It only allows the user to produce parts for their team."""
        user = self.request.user
        part_name = serializer.validated_data["name"]
        team = user.team

        if not team:
            raise ValidationError({"error": "Bir takıma atanmış olmalısınız!"})

        part = self.service.create_part(
            name=part_name,
            aircraft=serializer.validated_data["aircraft"],
            team=team,
        )
        serializer.instance = part

    def perform_destroy(self, instance):
        """The user can only delete parts belonging to her own team."""
        user = self.request.user

        if instance.team != user.team and not user.is_staff:
            raise ValidationError(
                {
                    "error": "Yalnızca kendi takımınıza ait parçaları silebilirsiniz!"
                }
            )
        self.service.delete_part(instance)


class InventoryViewSet(viewsets.ModelViewSet):
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]
    service = InventoryService()

    def get_queryset(self):
        return self.service.get_inventory()

    @action(detail=False, methods=["get"])
    def missing_parts(self, request):
        """Endpoint listing missing parts"""
        missing = self.service.get_missing_parts()
        return Response({"missing_parts": missing})


class AssemblyViewSet(viewsets.ModelViewSet):
    serializer_class = AssemblySerializer
    permission_classes = [IsAuthenticated]
    service = AssemblyService()

    def get_queryset(self):
        """The assembly team and admin can see the produced aircraft."""
        user = self.request.user
        if user.is_staff or user.team.name == TeamChoices.ASSEMBLY:
            return self.service.get_all()
        return self.service.get_all().none()

    @action(detail=False, methods=["post"])
    def assemble(self, request):
        """Starts the assembly process"""
        user = request.user
        aircraft_id = request.data.get("aircraft")

        try:
            aircraft = Aircraft.objects.get(id=aircraft_id)
        except Aircraft.DoesNotExist:
            return Response(
                {"error": "Geçersiz uçak!"}, status=status.HTTP_400_BAD_REQUEST
            )

        result, status_code = self.service.assemble_aircraft(aircraft, user)

        if isinstance(result, dict) and "error" in result:
            return Response(result, status=status_code)

        return Response(AssemblySerializer(result).data, status=status_code)
