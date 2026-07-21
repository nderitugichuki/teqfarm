import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("daily_records", "0001_initial"), ("inventory", "0001_initial")]
    operations = [
        migrations.AddField(model_name="dailyfarmrecord", name="feed_item",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="daily_feed_records", to="inventory.inventoryitem")),
        migrations.AddField(model_name="dailyfarmrecord", name="feed_transaction",
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="daily_feed_record", to="inventory.stocktransaction")),
    ]
