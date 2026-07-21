from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from apps.common.permissions import IsManagerOrReadOnly
from apps.common.viewsets import AuditedModelViewSet
from .models import FeedIssue, FeedPurchase, FeedSupplier
from .serializers import FeedIssueSerializer, FeedPurchaseSerializer, FeedSupplierSerializer

class FeedSupplierViewSet(AuditedModelViewSet):
    permission_classes = (IsManagerOrReadOnly,)
    serializer_class = FeedSupplierSerializer
    queryset = FeedSupplier.objects.all()
    search_fields = ("name", "phone_number", "email")

class FeedPurchaseViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = (IsManagerOrReadOnly,)
    serializer_class = FeedPurchaseSerializer
    queryset = FeedPurchase.objects.select_related("item", "supplier", "created_by")
    filterset_fields = ("item", "supplier", "purchase_date")

class FeedIssueViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = (IsManagerOrReadOnly,)
    serializer_class = FeedIssueSerializer
    queryset = FeedIssue.objects.select_related("item", "batch", "created_by")
    filterset_fields = ("item", "batch", "issue_date")
