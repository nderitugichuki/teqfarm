from django.db import models
from apps.common.models import AuditedModel

class Vaccination(AuditedModel):
    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Scheduled"
        COMPLETED = "completed", "Completed"
        MISSED = "missed", "Missed"
    batch = models.ForeignKey("flocks.FlockBatch", on_delete=models.PROTECT, related_name="vaccinations")
    vaccine = models.ForeignKey("inventory.InventoryItem", on_delete=models.PROTECT, related_name="vaccinations")
    scheduled_date = models.DateField(db_index=True)
    administered_date = models.DateField(blank=True, null=True)
    dose_quantity = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED, db_index=True)
    notes = models.TextField(blank=True)
    stock_transaction = models.OneToOneField("inventory.StockTransaction", on_delete=models.PROTECT, blank=True, null=True, related_name="vaccination")

class MedicationRecord(AuditedModel):
    batch = models.ForeignKey("flocks.FlockBatch", on_delete=models.PROTECT, related_name="medications")
    medicine = models.ForeignKey("inventory.InventoryItem", on_delete=models.PROTECT, related_name="medications")
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(blank=True, null=True)
    dosage = models.CharField(max_length=100)
    reason = models.TextField()
    quantity_used = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stock_transaction = models.OneToOneField(
        "inventory.StockTransaction", on_delete=models.PROTECT,
        blank=True, null=True, related_name="medication_record"
    )

class DiseaseRecord(AuditedModel):
    batch = models.ForeignKey("flocks.FlockBatch", on_delete=models.PROTECT, related_name="disease_records")
    disease_name = models.CharField(max_length=150)
    diagnosed_date = models.DateField(db_index=True)
    affected_birds = models.PositiveIntegerField(default=0)
    symptoms = models.TextField(blank=True)
    treatment = models.TextField(blank=True)
    resolved_date = models.DateField(blank=True, null=True)

class VetVisit(AuditedModel):
    batch = models.ForeignKey("flocks.FlockBatch", on_delete=models.PROTECT, related_name="vet_visits", blank=True, null=True)
    visit_date = models.DateField(db_index=True)
    veterinarian = models.CharField(max_length=150)
    reason = models.TextField()
    findings = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)
    follow_up_date = models.DateField(blank=True, null=True, db_index=True)
