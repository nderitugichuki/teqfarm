import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name="PoultryHouse",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=100, unique=True)),
                ("capacity", models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ("notes", models.TextField(blank=True)),
                ("is_active", models.BooleanField(db_index=True, default=True)),
                ("cleaning_interval_days", models.PositiveSmallIntegerField(default=14, validators=[django.core.validators.MinValueValidator(1)])),
                ("last_cleaned_at", models.DateField(blank=True, null=True)),
                ("next_cleaning_at", models.DateField(blank=True, db_index=True, null=True)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="farms_poultryhouse_created", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("name",)},
        )
    ]

