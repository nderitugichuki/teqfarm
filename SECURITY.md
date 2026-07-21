# Security policy

TeqFarm contains private farm, customer, financial, and health records. Do not report vulnerabilities in public issues or include production data, credentials, tokens, database dumps, receipts, or logs in source control.

Report suspected vulnerabilities directly to the system owner. Include the affected version, reproduction steps using non-production data, and likely impact.

Operational requirements:

- HTTPS is mandatory in production.
- Every user must have an individual account with the least privileged role.
- Secrets belong only in the untracked `.env` file or a managed secret store.
- PostgreSQL and application containers must not be publicly exposed.
- Backups must be encrypted, stored off-host, access-controlled, and restore-tested.
- Security and base-image updates should be tested and deployed promptly.

