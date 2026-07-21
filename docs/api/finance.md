# Sales and expenses API

## Sales

- `/api/v1/sales/customers/` manages customers.
- `/api/v1/sales/` creates and lists egg, live-bird, and manure sales.
- `/api/v1/sales/{id}/payment/` updates the cumulative amount paid and derives payment status.
- `/api/v1/sales/{id}/invoice/` returns a printable HTML invoice.
- `/api/v1/sales/{id}/receipt/` returns a printable HTML receipt.

Invoice numbers and totals are generated server-side. Egg and live-bird sales atomically reduce egg inventory or flock count. Sales are immutable after creation except for payment tracking.

## Expenses

- `/api/v1/expenses/` manages categorized expenses.
- Receipt uploads accept PDF, JPEG, PNG, or WebP files up to 5 MB.
- Administrators and managers can filter by category, date, and payment method.
