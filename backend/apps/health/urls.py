from rest_framework.routers import DefaultRouter
from .views import DiseaseRecordViewSet, MedicationRecordViewSet, VaccinationViewSet, VetVisitViewSet
router = DefaultRouter()
router.register("vaccinations", VaccinationViewSet)
router.register("medications", MedicationRecordViewSet)
router.register("diseases", DiseaseRecordViewSet)
router.register("vet-visits", VetVisitViewSet)
urlpatterns = router.urls
