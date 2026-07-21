from django.contrib import admin
from .models import FeedIssue, FeedPurchase, FeedSupplier
admin.site.register((FeedSupplier, FeedPurchase, FeedIssue))
