from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import InventoryItem, StockTransaction
from .services import record_stock_transaction


class InventoryItemSerializer(serializers.ModelSerializer):
    is_low_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = InventoryItem
        fields = "__all__"
        read_only_fields = ("current_stock", "created_by", "created_at", "updated_at")


class StockTransactionSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source="item.name", read_only=True)
    unit = serializers.CharField(source="item.unit", read_only=True)

    class Meta:
        model = StockTransaction
        fields = "__all__"
        read_only_fields = ("created_by", "created_at", "updated_at")

    def create(self, validated_data):
        try:
            return record_stock_transaction(
                created_by=self.context["request"].user, **validated_data
            )
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.message_dict) from exc

