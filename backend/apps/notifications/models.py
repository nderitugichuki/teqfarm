from django.conf import settings
from django.db import models
from apps.common.models import TimeStampedModel


class Notification(TimeStampedModel):
    class AlertType(models.TextChoices):
        LOW_STOCK = "low_stock", "Low Stock"
        EXPIRY = "expiry", "Expiring Stock"
        VACCINATION = "vaccination", "Vaccination Due"
        MORTALITY = "mortality", "High Mortality"
        CLEANING = "cleaning", "Cleaning Due"

    class Severity(models.TextChoices):
        INFO = "info", "Info"
        WARNING = "warning", "Warning"
        CRITICAL = "critical", "Critical"

    fingerprint = models.CharField(max_length=180, unique=True)
    alert_type = models.CharField(max_length=30, choices=AlertType.choices, db_index=True)
    severity = models.CharField(max_length=20, choices=Severity.choices, default=Severity.WARNING)
    title = models.CharField(max_length=180)
    message = models.TextField()
    due_date = models.DateField(blank=True, null=True, db_index=True)
    resource_type = models.CharField(max_length=50, blank=True)
    resource_id = models.PositiveBigIntegerField(blank=True, null=True)
    is_resolved = models.BooleanField(default=False, db_index=True)
    read_by = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="read_notifications")

    class Meta:
        ordering = ("is_resolved", "-created_at")

