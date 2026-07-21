from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from rest_framework import serializers
from apps.inventory.models import InventoryItem, StockTransaction
from apps.inventory.services import record_stock_transaction
from .models import DiseaseRecord, MedicationRecord, Vaccination, VetVisit

class VaccinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccination
        fields = "__all__"
        read_only_fields = ("stock_transaction", "created_by", "created_at", "updated_at")

    def validate_vaccine(self, value):
        if value.category != InventoryItem.Category.VACCINE:
            raise serializers.ValidationError("Select a vaccine inventory item.")
        return value

    @transaction.atomic
    def create(self, data):
        actor = self.context["request"].user
        stock = None
        if data.get("status") == Vaccination.Status.COMPLETED:
            if not data.get("administered_date") or data.get("dose_quantity", 0) <= 0:
                raise serializers.ValidationError("Completed vaccination requires date and dose.")
            try:
                stock = record_stock_transaction(
                    item=data["vaccine"], transaction_type=StockTransaction.TransactionType.STOCK_OUT,
                    quantity=data["dose_quantity"], transaction_date=data["administered_date"],
                    reference=data["batch"].batch_code, created_by=actor,
                )
            except DjangoValidationError as exc:
                raise serializers.ValidationError(exc.message_dict) from exc
        return Vaccination.objects.create(**data, stock_transaction=stock, created_by=actor)

    @transaction.atomic
    def update(self, instance, data):
        if instance.status == Vaccination.Status.COMPLETED:
            raise serializers.ValidationError("Completed vaccinations are immutable.")
        for field, value in data.items():
            setattr(instance, field, value)
        if instance.status == Vaccination.Status.COMPLETED:
            if not instance.administered_date or instance.dose_quantity <= 0:
                raise serializers.ValidationError("Completed vaccination requires date and dose.")
            try:
                instance.stock_transaction = record_stock_transaction(
                    item=instance.vaccine, transaction_type=StockTransaction.TransactionType.STOCK_OUT,
                    quantity=instance.dose_quantity, transaction_date=instance.administered_date,
                    reference=instance.batch.batch_code, created_by=self.context["request"].user,
                )
            except DjangoValidationError as exc:
                raise serializers.ValidationError(exc.message_dict) from exc
        instance.save()
        return instance

class MedicationRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicationRecord
        fields = "__all__"
        read_only_fields = ("stock_transaction", "created_by", "created_at", "updated_at")

    def validate_medicine(self, value):
        if value.category != InventoryItem.Category.MEDICINE:
            raise serializers.ValidationError("Select a medicine inventory item.")
        return value

    @transaction.atomic
    def create(self, data):
        actor = self.context["request"].user
        stock = None
        if data.get("quantity_used", 0) > 0:
            try:
                stock = record_stock_transaction(
                    item=data["medicine"], transaction_type=StockTransaction.TransactionType.STOCK_OUT,
                    quantity=data["quantity_used"], transaction_date=data["start_date"],
                    reference=data["batch"].batch_code, created_by=actor,
                )
            except DjangoValidationError as exc:
                raise serializers.ValidationError(exc.message_dict) from exc
        return MedicationRecord.objects.create(**data, stock_transaction=stock, created_by=actor)

class DiseaseRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseaseRecord
        fields = "__all__"
        read_only_fields = ("created_by", "created_at", "updated_at")

class VetVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = VetVisit
        fields = "__all__"
        read_only_fields = ("created_by", "created_at", "updated_at")
