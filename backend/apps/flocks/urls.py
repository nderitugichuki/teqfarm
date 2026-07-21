from rest_framework.routers import DefaultRouter

from .views import BirdMovementViewSet, BreedViewSet, FlockBatchViewSet, SupplierViewSet

router = DefaultRouter()
router.register("suppliers", SupplierViewSet)
router.register("breeds", BreedViewSet)
router.register("batches", FlockBatchViewSet)
router.register("movements", BirdMovementViewSet)

urlpatterns = router.urls

