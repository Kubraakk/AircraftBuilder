from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Kullanıcı adminse tüm yetkilere sahiptir.
    Admin değilse sadece okuma (GET) yetkisi vardır.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_staff


class IsTeamMember(BasePermission):
    """
    Kullanıcı yalnızca kendi takımına ait verileri yönetebilir.
    """

    def has_permission(self, request, view):
        return request.user and request.user.team is not None

    def has_object_permission(self, request, view, obj):
        return obj.team == request.user.team


class IsAssemblyTeam(BasePermission):
    """
    Sadece montaj ekibine özel yetki.
    Montaj ekibi uçakları oluşturabilir ve yönetebilir.
    Diğer herkes sadece listeleme yapabilir.
    """

    def has_permission(self, request, view):
        # Eğer sadece listeleme (GET) yapıyorsa herkes erişebilir
        if request.method in SAFE_METHODS:
            return True

        # Admin ise her şeye erişebilir
        if request.user.is_staff:
            return True

        # Sadece Montaj Takımı işlem yapabilir
        return request.user.team and request.user.team.name == "Montaj Takımı"

    def has_object_permission(self, request, view, obj):
        # Listeleme (GET) serbest
        if request.method in SAFE_METHODS:
            return True

        # Admin her şeyi yönetebilir
        if request.user.is_staff:
            return True

        # Montaj takımı uçağı yönetebilir
        return request.user.team.name == "Montaj Takımı"
