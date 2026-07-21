from django.contrib import admin
from django.db import connection
from django.http import JsonResponse
from django.urls import include, path


def healthcheck(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        cursor.fetchone()
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("health/", healthcheck, name="healthcheck"),
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("apps.accounts.urls")),
    path("api/v1/farm/", include("apps.farms.urls")),
    path("api/v1/flocks/", include("apps.flocks.urls")),
    path("api/v1/daily-records/", include("apps.daily_records.urls")),
    path("api/v1/inventory/", include("apps.inventory.urls")),
    path("api/v1/feed/", include("apps.feed.urls")),
    path("api/v1/eggs/", include("apps.eggs.urls")),
    path("api/v1/health/", include("apps.health.urls")),
    path("api/v1/sales/", include("apps.sales.urls")),
    path("api/v1/expenses/", include("apps.expenses.urls")),
    path("api/v1/dashboard/", include("apps.dashboard.urls")),
    path("api/v1/reports/", include("apps.reports.urls")),
    path("api/v1/notifications/", include("apps.notifications.urls")),
]
