import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("flocks", "0001_initial"),
    ]
    operations = [
        migrations.CreateModel(
            name="DailyFarmRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("record_date", models.DateField(db_index=True)),
                ("eggs_collected", models.PositiveIntegerField(default=0)),
                ("broken_eggs", models.PositiveIntegerField(default=0)),
                ("dirty_eggs", models.PositiveIntegerField(default=0)),
                ("feed_issued_kg", models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ("water_notes", models.TextField(blank=True)),
                ("sick_birds", models.PositiveIntegerField(default=0)),
                ("dead_birds", models.PositiveIntegerField(default=0)),
                ("observations", models.TextField(blank=True)),
                ("batch", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="daily_records", to="flocks.flockbatch")),
                ("mortality_movement", models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="daily_record", to="flocks.birdmovement")),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="daily_records_dailyfarmrecord_created", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ("-record_date", "batch__batch_code"),
                "constraints": [
                    models.UniqueConstraint(fields=("batch", "record_date"), name="unique_daily_record_per_batch"),
                    models.CheckConstraint(condition=models.Q(("broken_eggs__lte", models.F("eggs_collected"))), name="daily_broken_not_above_collected"),
                    models.CheckConstraint(condition=models.Q(("dirty_eggs__lte", models.F("eggs_collected"))), name="daily_dirty_not_above_collected"),
                ],
            },
        )
    ]

