import apps.sales.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL), ("flocks", "0001_initial")]
    operations = [
        migrations.CreateModel(name="Customer", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)), ("updated_at", models.DateTimeField(auto_now=True)),
            ("name", models.CharField(max_length=150)), ("phone_number", models.CharField(blank=True, max_length=30)), ("email", models.EmailField(blank=True, max_length=254)), ("address", models.TextField(blank=True)), ("notes", models.TextField(blank=True)), ("is_active", models.BooleanField(db_index=True, default=True)),
            ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="sales_customer_created", to=settings.AUTH_USER_MODEL)),
        ], options={"ordering": ("name",)}),
        migrations.CreateModel(name="Sale", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)), ("updated_at", models.DateTimeField(auto_now=True)),
            ("invoice_number", models.CharField(default=apps.sales.models.generate_invoice_number, max_length=40, unique=True)), ("sale_date", models.DateField(db_index=True, default=django.utils.timezone.localdate)), ("sale_type", models.CharField(choices=[("eggs", "Eggs"), ("live_birds", "Live Birds"), ("manure", "Manure")], db_index=True, max_length=20)), ("quantity", models.DecimalField(decimal_places=2, max_digits=14)), ("unit", models.CharField(max_length=30)), ("unit_price", models.DecimalField(decimal_places=2, max_digits=14)), ("total_amount", models.DecimalField(decimal_places=2, max_digits=16)), ("amount_paid", models.DecimalField(decimal_places=2, default=0, max_digits=16)), ("payment_method", models.CharField(choices=[("cash", "Cash"), ("mobile_money", "Mobile Money"), ("bank", "Bank Transfer"), ("credit", "Credit")], max_length=20)), ("payment_status", models.CharField(choices=[("paid", "Paid"), ("partial", "Partially Paid"), ("unpaid", "Unpaid")], db_index=True, max_length=20)), ("notes", models.TextField(blank=True)),
            ("customer", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="sales", to="sales.customer")), ("batch", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="sales", to="flocks.flockbatch")), ("bird_movement", models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="sale", to="flocks.birdmovement")), ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="sales_sale_created", to=settings.AUTH_USER_MODEL)),
        ], options={"ordering": ("-sale_date", "-created_at")}),
    ]
