import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL), ("daily_records", "0001_initial"), ("flocks", "0001_initial")]
    operations = [
        migrations.CreateModel(name="EggInventory", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)), ("updated_at", models.DateTimeField(auto_now=True)), ("good_eggs", models.PositiveIntegerField(default=0)), ("broken_eggs", models.PositiveIntegerField(default=0)), ("dirty_eggs", models.PositiveIntegerField(default=0)), ("trays_available", models.PositiveIntegerField(default=0)), ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="eggs_egginventory_created", to=settings.AUTH_USER_MODEL))]),
        migrations.CreateModel(name="EggProduction", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)), ("updated_at", models.DateTimeField(auto_now=True)), ("production_date", models.DateField(db_index=True)), ("good_eggs", models.PositiveIntegerField(default=0)), ("broken_eggs", models.PositiveIntegerField(default=0)), ("dirty_eggs", models.PositiveIntegerField(default=0)), ("batch", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="egg_production", to="flocks.flockbatch")), ("daily_record", models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name="egg_production", to="daily_records.dailyfarmrecord")), ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="eggs_eggproduction_created", to=settings.AUTH_USER_MODEL))]),
    ]
