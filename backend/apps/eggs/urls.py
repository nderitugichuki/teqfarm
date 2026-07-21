from rest_framework.routers import DefaultRouter
from .views import EggInventoryViewSet, EggProductionViewSet
router = DefaultRouter()
router.register("inventory", EggInventoryViewSet)
router.register("production", EggProductionViewSet)
urlpatterns = router.urls
