from apps.common.permissions import IsManagerOrReadOnly
from apps.common.viewsets import AuditedModelViewSet
from rest_framework.exceptions import MethodNotAllowed
from .models import DiseaseRecord, MedicationRecord, Vaccination, VetVisit
from .serializers import DiseaseRecordSerializer, MedicationRecordSerializer, VaccinationSerializer, VetVisitSerializer

class VaccinationViewSet(AuditedModelViewSet):
    permission_classes = (IsManagerOrReadOnly,)
    serializer_class = VaccinationSerializer
    queryset = Vaccination.objects.select_related("batch", "vaccine", "created_by")
    filterset_fields = ("batch", "status", "scheduled_date", "administered_date")
    def perform_create(self, serializer): serializer.save()
    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed("DELETE", detail="Vaccination history cannot be deleted.")

class MedicationRecordViewSet(AuditedModelViewSet):
    permission_classes = (IsManagerOrReadOnly,)
    serializer_class = MedicationRecordSerializer
    queryset = MedicationRecord.objects.select_related("batch", "medicine", "created_by")
    filterset_fields = ("batch", "medicine", "start_date")
    def perform_create(self, serializer): serializer.save()
    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method, detail="Medication usage records are immutable.")
    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed("DELETE", detail="Medication usage records are immutable.")

class DiseaseRecordViewSet(AuditedModelViewSet):
    permission_classes = (IsManagerOrReadOnly,)
    serializer_class = DiseaseRecordSerializer
    queryset = DiseaseRecord.objects.select_related("batch", "created_by")
    filterset_fields = ("batch", "diagnosed_date", "resolved_date")

class VetVisitViewSet(AuditedModelViewSet):
    permission_classes = (IsManagerOrReadOnly,)
    serializer_class = VetVisitSerializer
    queryset = VetVisit.objects.select_related("batch", "created_by")
    filterset_fields = ("batch", "visit_date", "follow_up_date")
