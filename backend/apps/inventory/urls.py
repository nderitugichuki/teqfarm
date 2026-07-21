from rest_framework.routers import DefaultRouter

from .views import InventoryItemViewSet, StockTransactionViewSet

router = DefaultRouter()
router.register("items", InventoryItemViewSet)
router.register("transactions", StockTransactionViewSet)
urlpatterns = router.urls

