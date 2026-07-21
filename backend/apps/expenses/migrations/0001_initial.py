import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [migrations.CreateModel(name="Expense", fields=[
        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)), ("updated_at", models.DateTimeField(auto_now=True)),
        ("expense_date", models.DateField(db_index=True, default=django.utils.timezone.localdate)), ("category", models.CharField(choices=[("feed", "Feed"), ("medicine", "Medicine"), ("labour", "Labour"), ("electricity", "Electricity"), ("water", "Water"), ("repairs", "Repairs"), ("fuel", "Fuel"), ("miscellaneous", "Miscellaneous")], db_index=True, max_length=20)), ("description", models.CharField(max_length=255)), ("payee", models.CharField(blank=True, max_length=150)), ("amount", models.DecimalField(decimal_places=2, max_digits=16, validators=[django.core.validators.MinValueValidator(0.01)])), ("payment_method", models.CharField(choices=[("cash", "Cash"), ("mobile_money", "Mobile Money"), ("bank", "Bank Transfer"), ("credit", "Credit")], max_length=20)), ("reference", models.CharField(blank=True, max_length=100)), ("receipt", models.FileField(blank=True, null=True, upload_to="expense_receipts/%Y/%m/", validators=[django.core.validators.FileExtensionValidator(("pdf", "jpg", "jpeg", "png", "webp"))])), ("notes", models.TextField(blank=True)),
        ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="expenses_expense_created", to=settings.AUTH_USER_MODEL)),
    ], options={"ordering": ("-expense_date", "-created_at")})]
