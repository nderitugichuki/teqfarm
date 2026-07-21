from rest_framework.routers import DefaultRouter

from .views import PoultryHouseViewSet

router = DefaultRouter()
router.register("houses", PoultryHouseViewSet, basename="house")

urlpatterns = router.urls

