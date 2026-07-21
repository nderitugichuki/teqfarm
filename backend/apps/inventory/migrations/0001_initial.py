import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name="InventoryItem", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)), ("updated_at", models.DateTimeField(auto_now=True)),
            ("name", models.CharField(max_length=150, unique=True)), ("sku", models.CharField(max_length=50, unique=True)), ("category", models.CharField(choices=[("feed", "Feed"), ("medicine", "Medicine"), ("vaccine", "Vaccine"), ("egg_tray", "Egg Tray"), ("equipment", "Equipment")], db_index=True, max_length=20)), ("unit", models.CharField(max_length=30)), ("current_stock", models.DecimalField(decimal_places=2, default=0, max_digits=14)), ("reorder_level", models.DecimalField(decimal_places=2, default=0, max_digits=14, validators=[django.core.validators.MinValueValidator(0)])), ("is_active", models.BooleanField(db_index=True, default=True)), ("notes", models.TextField(blank=True)),
            ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="inventory_inventoryitem_created", to=settings.AUTH_USER_MODEL)),
        ], options={"ordering": ("category", "name")}),
        migrations.CreateModel(name="StockTransaction", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)), ("updated_at", models.DateTimeField(auto_now=True)),
            ("transaction_type", models.CharField(choices=[("in", "Stock In"), ("out", "Stock Out"), ("adjustment_in", "Adjustment In"), ("adjustment_out", "Adjustment Out")], db_index=True, max_length=20)), ("quantity", models.DecimalField(decimal_places=2, max_digits=14, validators=[django.core.validators.MinValueValidator(0.01)])), ("transaction_date", models.DateField(db_index=True)), ("expiry_date", models.DateField(blank=True, db_index=True, null=True)), ("unit_cost", models.DecimalField(decimal_places=2, default=0, max_digits=14)), ("reference", models.CharField(blank=True, max_length=100)), ("notes", models.TextField(blank=True)),
            ("item", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="transactions", to="inventory.inventoryitem")), ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="inventory_stocktransaction_created", to=settings.AUTH_USER_MODEL)),
        ], options={"ordering": ("-transaction_date", "-created_at")}),
    ]
