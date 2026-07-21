import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("farms", "0001_initial"),
    ]
    operations = [
        migrations.CreateModel(
            name="Breed",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="flocks_breed_created", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("name",)},
        ),
        migrations.CreateModel(
            name="Supplier",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=150, unique=True)),
                ("contact_person", models.CharField(blank=True, max_length=100)),
                ("phone_number", models.CharField(blank=True, max_length=30)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("notes", models.TextField(blank=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="flocks_supplier_created", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("name",)},
        ),
        migrations.CreateModel(
            name="FlockBatch",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("batch_code", models.CharField(max_length=40, unique=True)),
                ("batch_name", models.CharField(max_length=120)),
                ("bird_type", models.CharField(choices=[("layers", "Layers"), ("broilers", "Broilers"), ("kienyeji", "Kienyeji"), ("breeders", "Breeders")], db_index=True, max_length=20)),
                ("arrival_date", models.DateField()),
                ("initial_bird_count", models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ("current_bird_count", models.PositiveIntegerField(default=0)),
                ("purchase_cost", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ("status", models.CharField(choices=[("planned", "Planned"), ("active", "Active"), ("quarantined", "Quarantined"), ("closed", "Closed")], db_index=True, default="active", max_length=20)),
                ("notes", models.TextField(blank=True)),
                ("breed", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="batches", to="flocks.breed")),
                ("supplier", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="batches", to="flocks.supplier")),
                ("poultry_house", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="batches", to="farms.poultryhouse")),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="flocks_flockbatch_created", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ("-arrival_date", "batch_code"),
                "constraints": [models.CheckConstraint(condition=models.Q(("current_bird_count__lte", models.F("initial_bird_count"))), name="flock_current_not_above_initial")],
            },
        ),
        migrations.CreateModel(
            name="BirdMovement",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("movement_type", models.CharField(choices=[("arrival", "Arrival"), ("mortality", "Mortality"), ("sale", "Sale"), ("adjustment_in", "Adjustment In"), ("adjustment_out", "Adjustment Out")], db_index=True, max_length=20)),
                ("quantity", models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ("movement_date", models.DateField(db_index=True)),
                ("reference", models.CharField(blank=True, max_length=100)),
                ("notes", models.TextField(blank=True)),
                ("batch", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="bird_movements", to="flocks.flockbatch")),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="flocks_birdmovement_created", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("-movement_date", "-created_at")},
        ),
    ]

