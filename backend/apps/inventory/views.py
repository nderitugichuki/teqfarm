from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from apps.common.permissions import IsManagerOrReadOnly
from apps.common.viewsets import AuditedModelViewSet

from .models import InventoryItem, StockTransaction
from .serializers import InventoryItemSerializer, StockTransactionSerializer


class InventoryItemViewSet(AuditedModelViewSet):
    permission_classes = (IsManagerOrReadOnly,)
    serializer_class = InventoryItemSerializer
    queryset = InventoryItem.objects.select_related("created_by")
    filterset_fields = ("category", "is_active")
    search_fields = ("name", "sku", "notes")
    ordering_fields = ("name", "category", "current_stock", "reorder_level")

    def destroy(self, request, *args, **kwargs):
        item = self.get_object()
        item.is_active = False
        item.save(update_fields=("is_active", "updated_at"))
        from rest_framework.response import Response

        return Response(status=204)


class StockTransactionViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = (IsManagerOrReadOnly,)
    serializer_class = StockTransactionSerializer
    queryset = StockTransaction.objects.select_related("item", "created_by")
    filterset_fields = ("item", "item__category", "transaction_type", "transaction_date", "expiry_date")
    search_fields = ("item__name", "item__sku", "reference")
    ordering_fields = ("transaction_date", "quantity", "expiry_date", "created_at")

