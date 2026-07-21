# Authentication API

Base path: `/api/v1/auth/`

All authenticated endpoints expect `Authorization: Bearer <access-token>`.

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `login/` | Authenticate with username and password; return access token, refresh token, and user profile |
| POST | `refresh/` | Rotate a valid refresh token |
| POST | `verify/` | Verify a token |
| POST | `logout/` | Blacklist a refresh token |
| GET | `profile/` | Read the authenticated user's profile |
| PATCH | `profile/` | Update editable profile fields |
| POST | `change-password/` | Validate the current password and set a new password |

## Roles

- `administrator`: full system administration
- `manager`: operational management and reporting
- `worker`: daily farm data entry

Authorization is enforced on the API. Shared permission classes live in `apps.common.permissions`.

