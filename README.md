# TeqFarm

TeqFarm is a responsive poultry farm management system for a single farm. The planned stack is Django, Django REST Framework, PostgreSQL, React, Vite, Tailwind CSS, Docker Compose, and Nginx.

## Delivery phases

1. Repository architecture and folder scaffold (current phase)
2. Backend foundation, authentication, roles, and audit trail
3. Poultry houses, flocks, and daily records
4. Feed, eggs, health, and inventory
5. Sales, expenses, invoices, and file uploads
6. Dashboard, notifications, and reporting exports
7. Responsive React application and role-aware workflows
8. Automated tests, observability, security hardening, and deployment

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the complete project layout and module boundaries.

## Backend development

Requires Python 3.12+ and PostgreSQL.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".\backend[dev]"
Copy-Item .env.example .env
.\.venv\Scripts\python.exe backend\manage.py migrate
.\.venv\Scripts\python.exe backend\manage.py createsuperuser
.\.venv\Scripts\python.exe backend\manage.py runserver
```

Run backend checks and tests:

```powershell
Set-Location backend
..\.venv\Scripts\python.exe manage.py check --settings=config.settings.test
..\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run --settings=config.settings.test
..\.venv\Scripts\python.exe -m pytest
```

Authentication API documentation is in [docs/api/authentication.md](docs/api/authentication.md).
Farm operations API documentation is in [docs/api/farm-operations.md](docs/api/farm-operations.md).
Stock and health API documentation is in [docs/api/stock-and-health.md](docs/api/stock-and-health.md).
Finance API documentation is in [docs/api/finance.md](docs/api/finance.md).
Dashboard and reporting documentation is in [docs/api/dashboard-reports.md](docs/api/dashboard-reports.md).
Frontend architecture and development instructions are in [docs/frontend.md](docs/frontend.md).

Production deployment instructions are in [docs/deployment/production.md](docs/deployment/production.md), with incident procedures in [docs/deployment/runbook.md](docs/deployment/runbook.md).
