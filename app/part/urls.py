from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PartViewSet, InventoryViewSet, AssemblyViewSet

router = DefaultRouter()
router.register(r"parts", PartViewSet)
router.register(r"inventory", InventoryViewSet)
router.register(r"assembly", AssemblyViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
