from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone
from rest_framework import serializers

from .models import DailyFarmRecord
from .services import create_daily_record, update_daily_record


class DailyFarmRecordSerializer(serializers.ModelSerializer):
    batch_code = serializers.CharField(source="batch.batch_code", read_only=True)
    poultry_house_name = serializers.CharField(source="batch.poultry_house.name", read_only=True)
    good_eggs = serializers.IntegerField(read_only=True)
    recorded_by = serializers.CharField(source="created_by.get_full_name", read_only=True)

    class Meta:
        model = DailyFarmRecord
        fields = (
            "id", "batch", "batch_code", "poultry_house_name", "record_date",
            "eggs_collected", "good_eggs", "broken_eggs", "dirty_eggs", "feed_issued_kg",
            "feed_item", "feed_transaction",
            "water_notes", "sick_birds", "dead_birds", "observations",
            "mortality_movement", "recorded_by", "created_by", "created_at", "updated_at",
        )
        read_only_fields = (
            "id", "mortality_movement", "feed_transaction", "created_by", "created_at", "updated_at"
        )

    def validate_record_date(self, value):
        if value > timezone.localdate():
            raise serializers.ValidationError("Daily records cannot be entered for a future date.")
        return value

    def validate(self, attrs):
        attrs = super().validate(attrs)
        collected = attrs.get("eggs_collected", getattr(self.instance, "eggs_collected", 0))
        broken = attrs.get("broken_eggs", getattr(self.instance, "broken_eggs", 0))
        dirty = attrs.get("dirty_eggs", getattr(self.instance, "dirty_eggs", 0))
        feed = attrs.get("feed_issued_kg", getattr(self.instance, "feed_issued_kg", 0))
        feed_item = attrs.get("feed_item", getattr(self.instance, "feed_item", None))
        if broken + dirty > collected:
            raise serializers.ValidationError(
                {"eggs_collected": "Collected eggs must cover broken and dirty eggs."}
            )
        if feed > 0 and not feed_item:
            raise serializers.ValidationError({"feed_item": "Select the feed item issued."})
        if feed_item and feed_item.category != "feed":
            raise serializers.ValidationError({"feed_item": "Select a feed inventory item."})
        return attrs

    def create(self, validated_data):
        try:
            return create_daily_record(
                created_by=self.context["request"].user, **validated_data
            )
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.message_dict) from exc

    def update(self, instance, validated_data):
        try:
            return update_daily_record(
                instance=instance, actor=self.context["request"].user, **validated_data
            )
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.message_dict) from exc
