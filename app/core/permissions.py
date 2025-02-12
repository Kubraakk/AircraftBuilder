from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    If the user is admin, he has all permissions.
    If there is not admin, there is only read (GET) permission.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_staff


class IsTeamMember(BasePermission):
    """
    The user can only manage data belonging to her own team.
    """

    def has_permission(self, request, view):
        return request.user and request.user.team is not None

    def has_object_permission(self, request, view, obj):
        return obj.team == request.user.team


class IsAssemblyTeam(BasePermission):
    """
    Special authority only for the assembly team.
    The assembly team can build and manage planes.
    Everyone else can just list.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_staff:
            return True
        return request.user.team and request.user.team.name == "Montaj Takımı"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_staff:
            return True
        return request.user.team.name == "Montaj Takımı"
