from django.contrib import admin
from .models import Customer, Sale
admin.site.register(Customer)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "sale_date", "sale_type", "customer", "total_amount", "payment_status")
    list_filter = ("sale_type", "payment_status", "sale_date")
    search_fields = ("invoice_number", "customer__name")
    readonly_fields = ("invoice_number", "total_amount", "bird_movement")

