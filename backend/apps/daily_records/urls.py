from rest_framework.routers import DefaultRouter

from .views import DailyFarmRecordViewSet

router = DefaultRouter()
router.register("", DailyFarmRecordViewSet, basename="daily-record")

urlpatterns = router.urls

