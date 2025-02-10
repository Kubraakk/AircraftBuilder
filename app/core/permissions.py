from rest_framework.permissions import BasePermission


class IsTeamMember(BasePermission):
    """
    Kullanıcının kendi takımına ait işlemleri yapmasını sağlar.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            obj.team == request.user.team
        )  # Sadece kendi takımının parçalarını yönetebilir
