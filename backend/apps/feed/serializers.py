from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from rest_framework import serializers

from apps.inventory.models import InventoryItem, StockTransaction
from apps.inventory.services import record_stock_transaction

from .models import FeedIssue, FeedPurchase, FeedSupplier


class FeedSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedSupplier
        fields = "__all__"
        read_only_fields = ("created_by", "created_at", "updated_at")


class FeedPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedPurchase
        fields = "__all__"
        read_only_fields = ("stock_transaction", "created_by", "created_at", "updated_at")

    def validate_item(self, value):
        if value.category != InventoryItem.Category.FEED:
            raise serializers.ValidationError("Select a feed inventory item.")
        return value

    @transaction.atomic
    def create(self, data):
        actor = self.context["request"].user
        try:
            stock = record_stock_transaction(
                item=data["item"], transaction_type=StockTransaction.TransactionType.STOCK_IN,
                quantity=data["quantity_kg"], transaction_date=data["purchase_date"],
                unit_cost=data["unit_cost"], reference=data.get("invoice_number", ""), created_by=actor,
            )
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.message_dict) from exc
        return FeedPurchase.objects.create(**data, stock_transaction=stock, created_by=actor)


class FeedIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedIssue
        fields = "__all__"
        read_only_fields = ("stock_transaction", "created_by", "created_at", "updated_at")

    def validate_item(self, value):
        if value.category != InventoryItem.Category.FEED:
            raise serializers.ValidationError("Select a feed inventory item.")
        return value

    @transaction.atomic
    def create(self, data):
        actor = self.context["request"].user
        try:
            stock = record_stock_transaction(
                item=data["item"], transaction_type=StockTransaction.TransactionType.STOCK_OUT,
                quantity=data["quantity_kg"], transaction_date=data["issue_date"],
                reference=data["batch"].batch_code, notes=data.get("notes", ""), created_by=actor,
            )
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.message_dict) from exc
        return FeedIssue.objects.create(**data, stock_transaction=stock, created_by=actor)
