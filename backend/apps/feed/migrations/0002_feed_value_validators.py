import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("feed", "0001_initial")]
    operations = [
        migrations.AlterField(
            model_name="feedpurchase",
            name="quantity_kg",
            field=models.DecimalField(
                decimal_places=2, max_digits=12,
                validators=[django.core.validators.MinValueValidator(0.01)],
            ),
        ),
        migrations.AlterField(
            model_name="feedpurchase",
            name="unit_cost",
            field=models.DecimalField(
                decimal_places=2, max_digits=12,
                validators=[django.core.validators.MinValueValidator(0)],
            ),
        ),
        migrations.AlterField(
            model_name="feedissue",
            name="quantity_kg",
            field=models.DecimalField(
                decimal_places=2, max_digits=12,
                validators=[django.core.validators.MinValueValidator(0.01)],
            ),
        ),
    ]
