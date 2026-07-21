from rest_framework.routers import DefaultRouter
from .views import FeedIssueViewSet, FeedPurchaseViewSet, FeedSupplierViewSet

router = DefaultRouter()
router.register("suppliers", FeedSupplierViewSet)
router.register("purchases", FeedPurchaseViewSet)
router.register("issues", FeedIssueViewSet)
urlpatterns = router.urls
