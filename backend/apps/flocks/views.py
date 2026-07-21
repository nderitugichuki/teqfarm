from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import GenericViewSet

from apps.common.permissions import IsAdministratorOrManager, IsManagerOrReadOnly
from apps.common.viewsets import AuditedModelViewSet

from .models import BirdMovement, Breed, FlockBatch, Supplier
from .serializers import (
    BirdMovementSerializer,
    BreedSerializer,
    FlockBatchSerializer,
    SupplierSerializer,
)


class SupplierViewSet(AuditedModelViewSet):
    permission_classes = (IsAdministratorOrManager,)
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()
    filterset_fields = ("is_active",)
    search_fields = ("name", "contact_person", "phone_number")


class BreedViewSet(AuditedModelViewSet):
    permission_classes = (IsAdministratorOrManager,)
    serializer_class = BreedSerializer
    queryset = Breed.objects.all()
    filterset_fields = ("is_active",)
    search_fields = ("name", "description")


class FlockBatchViewSet(AuditedModelViewSet):
    permission_classes = (IsManagerOrReadOnly,)
    serializer_class = FlockBatchSerializer
    queryset = FlockBatch.objects.select_related("breed", "supplier", "poultry_house", "created_by")
    filterset_fields = ("status", "bird_type", "breed", "supplier", "poultry_house")
    search_fields = ("batch_code", "batch_name", "breed__name", "supplier__name")
    ordering_fields = ("arrival_date", "current_bird_count", "batch_code", "created_at")

    def perform_create(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed("DELETE", detail="Close a flock batch instead of deleting its history.")


class BirdMovementViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = (IsManagerOrReadOnly,)
    serializer_class = BirdMovementSerializer
    queryset = BirdMovement.objects.select_related("batch", "created_by")
    filterset_fields = ("batch", "movement_type", "movement_date")
    ordering_fields = ("movement_date", "created_at", "quantity")
