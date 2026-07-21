from django.utils import timezone
from rest_framework import serializers
from .models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source="get_category_display", read_only=True)

    class Meta:
        model = Expense
        fields = "__all__"
        read_only_fields = ("created_by", "created_at", "updated_at")

    def validate_expense_date(self, value):
        if value > timezone.localdate():
            raise serializers.ValidationError("Expense date cannot be in the future.")
        return value

    def validate_receipt(self, value):
        if value and value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Receipt must not exceed 5 MB.")
        allowed_types = {"application/pdf", "image/jpeg", "image/png", "image/webp"}
        if value and getattr(value, "content_type", None) not in allowed_types:
            raise serializers.ValidationError("Receipt must be a PDF, JPEG, PNG, or WebP file.")
        return value

