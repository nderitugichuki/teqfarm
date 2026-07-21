# TeqFarm frontend

The React client is mobile-first and uses a role-aware navigation shell, reusable resource tables/forms, protected routes, Axios JWT refresh, loading and error states, and toast feedback.

## Local development

```powershell
Set-Location frontend
npm install
npm run dev
```

Set `VITE_API_URL=/api/v1` when the frontend and API share a host. Vite proxies `/api` and `/media` to Django during local development.

## Verification

```powershell
npm run lint
npm test
npm run build
```

The responsive breakpoints support phone data entry, tablet operation, and desktop management. Financial routes are hidden from workers and also protected by backend permissions.

Daily records select the feed inventory item used, allowing the backend to reconcile feed stock atomically with the worker's phone submission.
