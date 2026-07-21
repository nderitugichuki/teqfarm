from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from apps.common.permissions import IsAdministratorOrManager
from apps.common.viewsets import AuditedModelViewSet
from .models import Customer, Sale
from .serializers import CustomerSerializer, SalePaymentSerializer, SaleSerializer
from .services import update_sale_payment


class CustomerViewSet(AuditedModelViewSet):
    permission_classes = (IsAdministratorOrManager,)
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    filterset_fields = ("is_active",)
    search_fields = ("name", "phone_number", "email")

    def destroy(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.is_active = False
        customer.save(update_fields=("is_active", "updated_at"))
        return Response(status=status.HTTP_204_NO_CONTENT)


class SaleViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = (IsAdministratorOrManager,)
    serializer_class = SaleSerializer
    queryset = Sale.objects.select_related("customer", "batch", "created_by", "bird_movement")
    filterset_fields = ("sale_type", "customer", "batch", "sale_date", "payment_status", "payment_method")
    search_fields = ("invoice_number", "customer__name", "customer__phone_number")
    ordering_fields = ("sale_date", "total_amount", "amount_paid", "created_at")

    @action(detail=True, methods=("post",), url_path="payment")
    def payment(self, request, pk=None):
        payment_serializer = SalePaymentSerializer(data=request.data)
        payment_serializer.is_valid(raise_exception=True)
        try:
            sale = update_sale_payment(sale=self.get_object(), **payment_serializer.validated_data)
        except DjangoValidationError as exc:
            raise ValidationError(exc.message_dict) from exc
        return Response(SaleSerializer(sale, context={"request": request}).data)

    @action(detail=True, methods=("get",), url_path="invoice")
    def invoice(self, request, pk=None):
        html = render_to_string("sales/invoice.html", {"sale": self.get_object()})
        return HttpResponse(html, content_type="text/html", status=status.HTTP_200_OK)

    @action(detail=True, methods=("get",), url_path="receipt")
    def receipt(self, request, pk=None):
        html = render_to_string(
            "sales/invoice.html", {"sale": self.get_object(), "document_type": "Receipt"}
        )
        return HttpResponse(html, content_type="text/html", status=status.HTTP_200_OK)
