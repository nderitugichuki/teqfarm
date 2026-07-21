from django.contrib import admin
from .models import EggInventory, EggProduction
admin.site.register((EggInventory, EggProduction))
