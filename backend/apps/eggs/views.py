from rest_framework.viewsets import ReadOnlyModelViewSet
from apps.common.permissions import IsFarmStaff
from .models import EggInventory, EggProduction
from .serializers import EggInventorySerializer, EggProductionSerializer

class EggInventoryViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsFarmStaff,)
    serializer_class = EggInventorySerializer
    queryset = EggInventory.objects.all()

class EggProductionViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsFarmStaff,)
    serializer_class = EggProductionSerializer
    queryset = EggProduction.objects.select_related("batch", "daily_record", "created_by")
    filterset_fields = ("batch", "production_date")
    ordering_fields = ("production_date", "good_eggs")
