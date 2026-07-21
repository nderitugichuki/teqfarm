# Production acceptance checklist

Complete this checklist on a staging deployment before first production use.

## Platform

- All four containers report healthy and restart cleanly.
- `/health/` returns HTTP 200 and the frontend loads through Nginx.
- HTTPS redirects correctly and browsers report a valid certificate.
- PostgreSQL, backend port 8000, and frontend port 80 are not publicly exposed.
- A backup is created, copied off-host, and restored successfully in staging.

## Roles and authentication

- Administrator, manager, and worker accounts can log in.
- Workers cannot access sales, expenses, reports, administration, or write management endpoints.
- Managers can operate farm modules but cannot silently bypass backend validation.
- Password change invalidates the user's refresh session and login throttling activates after repeated failures.

## Operational transactions

- Creating a flock creates its arrival movement and respects house capacity.
- Daily mortality updates the flock count; correcting it reconciles the count.
- Daily feed entry decrements the selected feed item and rejects insufficient stock.
- Daily eggs update production and egg inventory.
- Egg and live-bird sales decrement the correct balance atomically.
- Vaccination and medication completion consumes the selected inventory item.
- Failed transactions leave all related balances unchanged.

## Finance and reports

- Sale totals, payment status, invoice, and receipt are correct.
- Expense receipt validation rejects unsupported or oversized files.
- Daily, weekly, monthly, operational, inventory, and profit/loss reports agree with source records.
- PDF and Excel downloads open successfully.

## Devices

- Daily entry is comfortable at 360 px width and with a phone keyboard.
- Navigation, tables, forms, and dialogs work on phone, tablet, and desktop.
- Loading, offline/error, empty, and validation states are understandable.
- Printable invoices fit A4 paper.

Record the application revision, tester, date, evidence, and any accepted exceptions before sign-off.

