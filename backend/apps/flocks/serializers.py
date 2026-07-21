from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import BirdMovement, Breed, FlockBatch, Supplier
from .services import create_batch, record_bird_movement


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"
        read_only_fields = ("created_by", "created_at", "updated_at")


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = "__all__"
        read_only_fields = ("created_by", "created_at", "updated_at")


class FlockBatchSerializer(serializers.ModelSerializer):
    breed_name = serializers.CharField(source="breed.name", read_only=True)
    supplier_name = serializers.CharField(source="supplier.name", read_only=True)
    poultry_house_name = serializers.CharField(source="poultry_house.name", read_only=True)

    class Meta:
        model = FlockBatch
        fields = (
            "id", "batch_code", "batch_name", "bird_type", "breed", "breed_name",
            "supplier", "supplier_name", "arrival_date", "initial_bird_count",
            "current_bird_count", "purchase_cost", "poultry_house", "poultry_house_name",
            "status", "notes", "created_at", "updated_at", "created_by",
        )
        read_only_fields = ("current_bird_count", "created_at", "updated_at", "created_by")

    def create(self, validated_data):
        try:
            return create_batch(created_by=self.context["request"].user, **validated_data)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.message_dict) from exc

    def update(self, instance, validated_data):
        validated_data.pop("initial_bird_count", None)
        for field, value in validated_data.items():
            setattr(instance, field, value)
        try:
            instance.full_clean()
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.message_dict) from exc
        instance.save()
        return instance


class BirdMovementSerializer(serializers.ModelSerializer):
    batch_code = serializers.CharField(source="batch.batch_code", read_only=True)

    class Meta:
        model = BirdMovement
        fields = (
            "id", "batch", "batch_code", "movement_type", "quantity", "movement_date",
            "reference", "notes", "created_at", "created_by",
        )
        read_only_fields = ("id", "created_at", "created_by")

    def validate_movement_type(self, value):
        if value == BirdMovement.MovementType.ARRIVAL:
            raise serializers.ValidationError("Arrival movements are created with the batch.")
        return value

    def create(self, validated_data):
        try:
            return record_bird_movement(
                created_by=self.context["request"].user, **validated_data
            )
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.message_dict) from exc

