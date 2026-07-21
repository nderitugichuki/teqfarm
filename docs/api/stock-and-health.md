# Stock, production, and health API

- `/api/v1/inventory/items/` manages feed, medicine, vaccine, tray, and equipment items.
- `/api/v1/inventory/transactions/` records immutable stock in/out adjustments.
- `/api/v1/feed/suppliers/`, `purchases/`, and `issues/` manage feed operations.
- `/api/v1/eggs/inventory/` and `production/` expose balances derived from daily records.
- `/api/v1/health/vaccinations/`, `medications/`, `diseases/`, and `vet-visits/` manage flock health.

All stock-changing operations lock the inventory row and reject negative balances. Completed vaccination and medication usage records are immutable to preserve the audit ledger.
