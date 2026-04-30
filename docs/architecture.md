# Architecture

## Runtime topology

```text
Next.js client ──▶ FastAPI API ──▶ PostgreSQL
                    │
                    ├──▶ Redis ──▶ Celery worker
                    │
                    └──▶ Auth session storage (refresh token hashes)
```

## Responsibility split

- **`client/`** renders the product UI, manages the in-memory access token, and refreshes auth sessions via HttpOnly cookie.
- **`server/app/api/routes/`** exposes HTTP contracts and translates domain/service outcomes into API responses.
- **`server/app/services/`** owns business logic and data access orchestration.
- **`server/app/tasks/`** runs asynchronous prediction work outside the request cycle.
- **`server/app/models/`** defines persistence for users, players, stats, favorites, prediction jobs, and auth sessions.

## Access model

- **Public catalog:** `/api/players/*`
- **Protected user state:** `/api/auth/me`, `/api/favorites/*`, `/api/predictions/*`
- **Session strategy:** short-lived Bearer access token plus rotating refresh token in an HttpOnly cookie

This keeps product discovery friction low while protecting identity, user state, and expensive prediction workloads from abuse.
