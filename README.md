# Smart Insights Dashboard v2

A full-stack golf analytics platform built with **FastAPI**, **Next.js**, **PostgreSQL**, and **Redis** — containerized with Docker Compose.

Track player performance, spot trends, and manage your favorites with a clean, modern dashboard.

> 📌 **Status:** Phase 3.5 — Seeded data, polished UI, charts live

---

## Tech Stack

| Layer     | Technology                          |
|-----------|-------------------------------------|
| Frontend  | Next.js 15, React 19, TypeScript, Tailwind CSS |
| Backend   | FastAPI, Python 3.12, SQLAlchemy 2.0 |
| Database  | PostgreSQL 16, Alembic migrations   |
| Cache     | Redis 7                             |
| Auth      | JWT (python-jose), bcrypt           |
| Charts    | Recharts                            |
| Infra     | Docker, Docker Compose              |

---

## Features

- **User authentication** — register, login, JWT-protected routes
- **Player database** — 15 seeded professional golf players with stats
- **Performance charts** — scoring averages and strokes gained over time
- **Favorites system** — star players and track them from your dashboard
- **Analytics dashboard** — stat cards, player table, trend charts
- **REST API** — clean FastAPI backend with OpenAPI docs

---

## Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose

### 1. Clone and configure

```bash
git clone https://github.com/JonatanLiljeblad/Smart_Insight_Dashboard.git
cd Smart_Insight_Dashboard
cp .env.example .env
```

### 2. Start everything

```bash
make up
# or: docker compose up --build -d
```

### 3. Set up the database

```bash
make migrate   # run Alembic migrations
make seed      # populate with demo data (15 players + stats)
```

### 4. Verify

| Service    | URL                          |
|------------|------------------------------|
| Frontend   | http://localhost:3000         |
| Backend    | http://localhost:8000         |
| API Docs   | http://localhost:8000/docs    |
| Health     | http://localhost:8000/health  |

```bash
curl http://localhost:8000/health
# → {"status":"ok"}
```

### 5. Try it out

1. Open http://localhost:3000 and click **Get started**
2. Register an account
3. Browse the dashboard — players, stats, and charts are populated
4. Click a player to see their performance trend
5. Star players to add them to your favorites

### 6. Stop

```bash
make down
# or: docker compose down -v
```

---

## API Routes

| Method | Endpoint                     | Auth     | Description              |
|--------|------------------------------|----------|--------------------------|
| GET    | `/health`                    | Public   | Health check             |
| POST   | `/api/auth/register`         | Public   | Register a new user      |
| POST   | `/api/auth/login`            | Public   | Login, returns JWT       |
| GET    | `/api/auth/me`               | Bearer   | Current user profile     |
| GET    | `/api/players/`              | Bearer   | List players             |
| GET    | `/api/players/{id}`          | Bearer   | Player detail            |
| GET    | `/api/players/{id}/stats`    | Bearer   | Player stat history      |
| GET    | `/api/favorites/`            | Bearer   | List user favorites      |
| POST   | `/api/favorites/`            | Bearer   | Add a favorite           |
| DELETE | `/api/favorites/{id}`        | Bearer   | Remove a favorite        |

Full interactive docs at http://localhost:8000/docs

---

## Development

### Makefile targets

| Command        | Description                        |
|----------------|------------------------------------|
| `make up`      | Build and start all services       |
| `make down`    | Stop and remove all services       |
| `make logs`    | Tail logs from all services        |
| `make migrate` | Run Alembic database migrations    |
| `make seed`    | Seed database with demo data       |
| `make test`    | Run backend test suite             |
| `make lint`    | Lint backend with ruff             |

### Run tests

```bash
make test
# 7 passed — health, register, login, auth, duplicates
```

### Run linter

```bash
make lint
# All checks passed!
```

---

## Project Structure

```
├── client/                # Next.js frontend
│   └── src/
│       ├── app/           # Pages (dashboard, login, register, players, favorites)
│       ├── components/    # UI components, auth, dashboard, charts
│       ├── hooks/         # useAuth, usePlayers, useFavorites
│       ├── services/      # API client layer
│       ├── lib/           # Shared utilities, auth helpers
│       └── types/         # TypeScript interfaces
├── server/                # FastAPI backend
│   ├── app/
│   │   ├── api/           # Routes (auth, players, favorites) + dependencies
│   │   ├── core/          # Config, security (JWT, bcrypt)
│   │   ├── db/            # SQLAlchemy engine, Base, session
│   │   ├── models/        # ORM models (User, Player, PlayerStat, Favorite)
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic (auth service)
│   │   └── main.py        # FastAPI app entrypoint
│   ├── alembic/           # Database migrations
│   ├── scripts/           # Seed data script
│   └── tests/             # Pytest suite
├── data/                  # Raw + processed datasets
├── ml/                    # ML notebooks, training, artifacts
├── docs/                  # Architecture docs, decisions
├── scripts/               # Project-level scripts
├── docker-compose.yml
├── .env.example
├── Makefile
└── README.md
```

---

## Environment Variables

Defined in `.env` (copy from `.env.example`):

| Variable                     | Description                        |
|------------------------------|------------------------------------|
| `POSTGRES_DB`                | Database name                      |
| `POSTGRES_USER`              | Database user                      |
| `POSTGRES_PASSWORD`          | Database password                  |
| `DATABASE_URL`               | Full connection string for backend |
| `REDIS_URL`                  | Redis connection string            |
| `JWT_SECRET`                 | Secret key for JWT tokens          |
| `JWT_ALGORITHM`              | JWT signing algorithm (HS256)      |
| `ACCESS_TOKEN_EXPIRE_MINUTES`| Token expiry in minutes            |
| `NEXT_PUBLIC_API_URL`        | Backend URL for frontend           |

> Docker Compose constructs `DATABASE_URL` and `REDIS_URL` automatically from the `POSTGRES_*` vars. The values in `.env` are used for local development without Docker.

---

## Ports

| Port | Service    |
|------|------------|
| 3000 | Frontend   |
| 8000 | Backend    |
| 5432 | PostgreSQL |
| 6379 | Redis      |

---

## Roadmap

- [x] Phase 1 — Foundation (Docker, health check, services running)
- [x] Phase 2 — Auth, database models, API routes, Alembic migrations
- [x] Phase 3 — Dashboard UI, data visualization, full-stack integration
- [x] Phase 3.5 — Seed data, polish, charts with real data
- [ ] Phase 4 — ML integration, predictions
- [ ] Phase 5 — Deployment, CI/CD, polish

---

## Author

**Jonatan Filip Liljeblad**
— CS & Math @ Albright College, Data Analytics minor
— [LinkedIn](https://www.linkedin.com/in/jonatan-liljeblad-690344260/) · [GitHub](https://github.com/JonatanLiljeblad)

## License

[MIT](LICENSE)
