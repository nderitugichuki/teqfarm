import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [migrations.CreateModel(name="Notification", fields=[
        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
        ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
        ("updated_at", models.DateTimeField(auto_now=True)),
        ("fingerprint", models.CharField(max_length=180, unique=True)),
        ("alert_type", models.CharField(choices=[("low_stock", "Low Stock"), ("expiry", "Expiring Stock"), ("vaccination", "Vaccination Due"), ("mortality", "High Mortality"), ("cleaning", "Cleaning Due")], db_index=True, max_length=30)),
        ("severity", models.CharField(choices=[("info", "Info"), ("warning", "Warning"), ("critical", "Critical")], default="warning", max_length=20)),
        ("title", models.CharField(max_length=180)), ("message", models.TextField()),
        ("due_date", models.DateField(blank=True, db_index=True, null=True)),
        ("resource_type", models.CharField(blank=True, max_length=50)),
        ("resource_id", models.PositiveBigIntegerField(blank=True, null=True)),
        ("is_resolved", models.BooleanField(db_index=True, default=False)),
        ("read_by", models.ManyToManyField(blank=True, related_name="read_notifications", to=settings.AUTH_USER_MODEL)),
    ], options={"ordering": ("is_resolved", "-created_at")})]
