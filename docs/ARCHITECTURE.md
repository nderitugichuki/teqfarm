# TeqFarm architecture

## Repository layout

```text
teqfarm/
|-- backend/
|   |-- config/                 # Django project settings, URLs, ASGI, WSGI
|   |   `-- settings/           # Base, development, test, production settings
|   |-- apps/
|   |   |-- common/             # Audit models, permissions, pagination, utilities
|   |   |-- accounts/           # Users, roles, profiles, JWT endpoints
|   |   |-- farms/              # Farm configuration and poultry houses
|   |   |-- flocks/             # Batches, breeds, suppliers, bird movements
|   |   |-- daily_records/      # Worker daily entries
|   |   |-- feed/               # Feed types, purchasing, issues, balances
|   |   |-- eggs/               # Egg production, inventory, movements
|   |   |-- health/             # Vaccines, medication, disease, vet, mortality
|   |   |-- inventory/          # General stock catalogue and transactions
|   |   |-- sales/              # Customers, sales, invoices, receipts
|   |   |-- expenses/           # Expense categories, expenses, attachments
|   |   |-- reports/            # Aggregation and PDF/Excel exports
|   |   |-- notifications/      # Alert rules and in-app notifications
|   |   `-- dashboard/          # Dashboard read models and chart endpoints
|   |-- templates/              # Printable invoice/report templates
|   |-- tests/                  # Cross-module integration and API tests
|   |-- manage.py
|   |-- pyproject.toml
|   `-- Dockerfile
|-- frontend/
|   |-- public/
|   |-- src/
|   |   |-- app/                # Router, providers, store setup
|   |   |-- assets/
|   |   |-- components/         # Reusable UI, forms, tables, charts, layout
|   |   |-- features/           # Domain screens, API hooks, feature components
|   |   |-- hooks/
|   |   |-- lib/                # Axios, validation, formatting, constants
|   |   |-- pages/              # Top-level route pages and error pages
|   |   |-- styles/
|   |   `-- test/               # Frontend test setup and fixtures
|   |-- tests/e2e/
|   |-- Dockerfile
|   `-- nginx.conf
|-- infrastructure/nginx/       # Production reverse proxy configuration
|-- scripts/                    # Operational scripts
|-- docs/                       # Architecture, API, deployment, decisions
|-- docker-compose.yml
`-- .env.example
```

## Backend module convention

Each domain app owns its models, serializers, API views, URLs, permissions, services, selectors, admin registration, migrations, and tests. Business mutations belong in transactional services; reporting and complex reads belong in selectors. API views remain thin.

## Frontend module convention

Each feature owns its API functions, query/mutation hooks, form schema, feature-specific components, and pages. Shared primitives stay in `components`, while authentication, routing, and global providers stay in `app`.

## Important invariants

- Bird counts change only through validated, transactional bird movements.
- Feed, egg, medicine, vaccine, and equipment balances derive from immutable stock transactions.
- Mortality and live-bird sales generate bird movements atomically.
- Audit fields are applied consistently, with actor information sourced from the authenticated request.
- Financial totals are calculated server-side with decimal arithmetic.
- Role checks are enforced by the API; the UI only mirrors those permissions for usability.

