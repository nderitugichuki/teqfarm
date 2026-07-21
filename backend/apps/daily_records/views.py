from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError
from apps.common.permissions import CanManageDailyRecords
from apps.common.viewsets import AuditedModelViewSet

from .models import DailyFarmRecord
from .serializers import DailyFarmRecordSerializer
from .services import delete_daily_record


class DailyFarmRecordViewSet(AuditedModelViewSet):
    permission_classes = (CanManageDailyRecords,)
    serializer_class = DailyFarmRecordSerializer
    queryset = DailyFarmRecord.objects.select_related(
        "batch", "batch__poultry_house", "created_by", "mortality_movement"
    )
    filterset_fields = ("batch", "batch__poultry_house", "record_date", "created_by")
    search_fields = ("batch__batch_code", "batch__batch_name", "observations")
    ordering_fields = ("record_date", "eggs_collected", "dead_birds", "created_at")

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == "worker" and not self.request.user.is_superuser:
            return queryset.filter(created_by=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        try:
            delete_daily_record(instance=instance)
        except DjangoValidationError as exc:
            raise ValidationError(exc.message_dict) from exc
