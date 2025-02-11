from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.part.views import PartViewSet, InventoryViewSet, AssemblyViewSet

router = DefaultRouter()
router.register(r"parts", PartViewSet, basename="part")
router.register(r"inventory", InventoryViewSet, basename="inventory")
router.register(r"assembly", AssemblyViewSet, basename="assembly")

urlpatterns = [
    path("", include(router.urls)),
]
