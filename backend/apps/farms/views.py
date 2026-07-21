from apps.common.permissions import IsManagerOrReadOnly
from apps.common.viewsets import AuditedModelViewSet

from .models import PoultryHouse
from .serializers import PoultryHouseSerializer


class PoultryHouseViewSet(AuditedModelViewSet):
    permission_classes = (IsManagerOrReadOnly,)
    serializer_class = PoultryHouseSerializer
    queryset = PoultryHouse.objects.select_related("created_by").all()
    filterset_fields = ("is_active",)
    search_fields = ("name", "notes")
    ordering_fields = ("name", "capacity", "next_cleaning_at", "created_at")
