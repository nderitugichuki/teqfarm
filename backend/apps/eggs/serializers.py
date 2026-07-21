from rest_framework import serializers
from .models import EggInventory, EggProduction

class EggInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EggInventory
        fields = "__all__"

class EggProductionSerializer(serializers.ModelSerializer):
    production_percentage = serializers.FloatField(read_only=True)
    batch_code = serializers.CharField(source="batch.batch_code", read_only=True)
    class Meta:
        model = EggProduction
        fields = "__all__"
