from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from .models import Customer, Sale
from .services import create_sale


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"
        read_only_fields = ("created_by", "created_at", "updated_at")


class SaleSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.name", read_only=True)
    batch_code = serializers.CharField(source="batch.batch_code", read_only=True)

    class Meta:
        model = Sale
        fields = "__all__"
        read_only_fields = (
            "invoice_number", "total_amount", "payment_status", "bird_movement", "created_by", "created_at", "updated_at"
        )

    def validate(self, attrs):
        paid = attrs.get("amount_paid", 0)
        if paid < 0:
            raise serializers.ValidationError({"amount_paid": "Payment cannot be negative."})
        return attrs

    def create(self, validated_data):
        try:
            return create_sale(created_by=self.context["request"].user, **validated_data)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.message_dict) from exc


class SalePaymentSerializer(serializers.Serializer):
    amount_paid = serializers.DecimalField(max_digits=16, decimal_places=2)
    payment_method = serializers.ChoiceField(choices=Sale.PaymentMethod.choices)
