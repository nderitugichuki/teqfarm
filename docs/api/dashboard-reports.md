# Dashboard, alerts, and reports

## Dashboard

`GET /api/v1/dashboard/` returns flock, house, egg, feed, mortality, vaccination, chart, and quick-action data. Financial summaries are returned only to administrators and managers.

## Notifications

- `GET /api/v1/notifications/` lists alerts.
- `POST /api/v1/notifications/{id}/read/` marks an alert as read for the current user.
- `POST /api/v1/notifications/refresh/` refreshes low-stock, expiry, vaccination, mortality, and cleaning alerts.

The refresh operation is idempotent and resolves alerts whose triggering condition has cleared.

## Reports

`GET /api/v1/reports/{type}/?start=YYYY-MM-DD&end=YYYY-MM-DD&format=json`

Supported types: `daily`, `weekly`, `monthly`, `production`, `mortality`, `feed`, `sales`, `expenses`, `profit-loss`, and `inventory`.

Set `format=xlsx` or `format=pdf` to download Excel or PDF output. Reports are restricted to administrators and managers.

