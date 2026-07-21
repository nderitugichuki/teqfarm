from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    is_read = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        exclude = ("read_by", "fingerprint")

    def get_is_read(self, obj):
        user = self.context["request"].user
        return any(reader.pk == user.pk for reader in obj.read_by.all())
