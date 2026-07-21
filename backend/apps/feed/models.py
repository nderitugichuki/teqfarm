from django.db import models
from django.core.validators import MinValueValidator
from apps.common.models import AuditedModel

class FeedSupplier(AuditedModel):
    name = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)

class FeedPurchase(AuditedModel):
    item = models.ForeignKey("inventory.InventoryItem", on_delete=models.PROTECT, related_name="feed_purchases")
    supplier = models.ForeignKey(FeedSupplier, on_delete=models.PROTECT, related_name="purchases")
    quantity_kg = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    purchase_date = models.DateField(db_index=True)
    invoice_number = models.CharField(max_length=80, blank=True)
    stock_transaction = models.OneToOneField("inventory.StockTransaction", on_delete=models.PROTECT, related_name="feed_purchase")

class FeedIssue(AuditedModel):
    item = models.ForeignKey("inventory.InventoryItem", on_delete=models.PROTECT, related_name="feed_issues")
    batch = models.ForeignKey("flocks.FlockBatch", on_delete=models.PROTECT, related_name="feed_issues")
    quantity_kg = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    issue_date = models.DateField(db_index=True)
    notes = models.TextField(blank=True)
    stock_transaction = models.OneToOneField("inventory.StockTransaction", on_delete=models.PROTECT, related_name="feed_issue")
