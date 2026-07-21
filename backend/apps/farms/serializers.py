from rest_framework import serializers

from .models import PoultryHouse


class PoultryHouseSerializer(serializers.ModelSerializer):
    current_occupancy = serializers.IntegerField(read_only=True)
    available_capacity = serializers.SerializerMethodField()

    class Meta:
        model = PoultryHouse
        fields = (
            "id",
            "name",
            "capacity",
            "current_occupancy",
            "available_capacity",
            "notes",
            "is_active",
            "cleaning_interval_days",
            "last_cleaned_at",
            "next_cleaning_at",
            "created_at",
            "updated_at",
            "created_by",
        )
        read_only_fields = ("id", "created_at", "updated_at", "created_by")

    def get_available_capacity(self, obj):
        return max(0, obj.capacity - obj.current_occupancy)

    def validate_capacity(self, value):
        if self.instance and value < self.instance.current_occupancy:
            raise serializers.ValidationError("Capacity cannot be below current occupancy.")
        return value

