from django.contrib import admin

from .models import InventoryItem, StockTransaction

admin.site.register(InventoryItem)
admin.site.register(StockTransaction)

