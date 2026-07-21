import pytest
from django.contrib.auth import get_user_model
from apps.inventory.models import InventoryItem
from apps.notifications.models import Notification
from apps.notifications.services import refresh_alerts

@pytest.mark.django_db
def test_alert_refresh_is_idempotent():
    user = get_user_model().objects.create_user(username="alerts", email="alerts@test.dev")
    InventoryItem.objects.create(name="Growers Mash", sku="GM-1", category="feed",
        unit="kg", current_stock=2, reorder_level=5, created_by=user)
    assert refresh_alerts() == 1
    assert refresh_alerts() == 1
    assert Notification.objects.filter(alert_type="low_stock", is_resolved=False).count() == 1

