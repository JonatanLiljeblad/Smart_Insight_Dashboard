# Smart Insights Dashboard

A full-stack analytics platform with integrated machine learning predictions and asynchronous job processing. Built to demonstrate production-grade system design — not just CRUD.

![Dashboard](docs/screenshots/dashboard.png)

---

## What it does

Users track professional golf players, analyze historical performance trends, and generate ML-powered scoring predictions — all through a modern dashboard backed by an async processing pipeline.

The system handles the full lifecycle: data ingestion → storage → API → async ML inference → real-time result delivery.

---

## Demo

Start locally and everything is running in under a minute:

| Service         | URL                         |
|-----------------|-----------------------------|
| Dashboard       | http://localhost:3000        |
| API             | http://localhost:8000        |
| Interactive Docs| http://localhost:8000/docs   |

![Player Detail](docs/screenshots/player-detail.png)

---

## Key Features

### Data & Analytics
- 15 seeded professional golf players with 180 historical stat records
- Performance trend charts (scoring average, strokes gained, GIR)
- Stat cards with real aggregated data
- Favorites system with per-user tracking

### Machine Learning
- **Prediction task:** forecast a player's next scoring average from recent performance
- Baseline model (LinearRegression) vs improved model (RandomForestRegressor)
- Feature engineering from sliding windows over 5 stat dimensions
- Model comparison: RMSE 0.63 → 0.62, saved as versioned artifact
- Predictions served through async job pipeline, not blocking API calls

### Async Processing
- Celery worker processes prediction jobs asynchronously
- Redis serves as both message broker and result backend
- Job lifecycle: `pending → running → completed/failed`
- Frontend polls job status and renders results on completion

### Authentication
- JWT-based auth with bcrypt password hashing
- Register / login / protected routes
- Token-based API access with Bearer scheme

---

## Architecture

```
┌────────────┐     ┌────────────┐     ┌────────────┐
│   Next.js  │────▶│  FastAPI    │────▶│ PostgreSQL │
│   :3000    │     │   :8000    │     │   :5432    │
└────────────┘     └─────┬──────┘     └────────────┘
                         │
                    ┌────▼─────┐
                    │  Redis   │
                    │  :6379   │
                    └────┬─────┘
                         │
                   ┌─────▼──────┐
                   │  Celery    │
                   │  Worker    │
                   └────────────┘
```

**5 Docker services** orchestrated via Compose:

| Service    | Role                              |
|------------|-----------------------------------|
| `client`   | Next.js frontend (SSR + SPA)      |
| `server`   | FastAPI REST API                  |
| `worker`   | Celery async task processor       |
| `db`       | PostgreSQL with persistent volume |
| `redis`    | Message broker + result backend   |

**Request flow for predictions:**
1. Client sends `POST /api/predictions/` with player ID
2. API creates a `PredictionJob` record (status: pending)
3. Celery task dispatched to worker via Redis
4. Worker loads trained model, builds features from recent stats, runs inference
5. Result written to DB, job marked completed
6. Client polls `GET /api/predictions/{id}` until result arrives

---

## ML Pipeline

```
Historical Stats → Feature Engineering → Model Training → Saved Artifact
                                                              │
Player Request → Recent Stats → Feature Vector → Inference → Prediction
```

| Component         | Detail                                      |
|-------------------|---------------------------------------------|
| Task              | Predict next scoring average                |
| Features          | 3-event rolling mean of 5 stat dimensions   |
| Baseline          | LinearRegression (RMSE: 0.6264)             |
| Improved          | RandomForestRegressor (RMSE: 0.6211)        |
| Training samples  | 135 (from 15 players × 12 events each)      |
| Artifact          | `scoring_model.joblib` (scikit-learn)       |

Train the model:

```bash
make train
```

---

## Tech Stack

| Layer      | Technologies                                            |
|------------|---------------------------------------------------------|
| Frontend   | Next.js 15, React 19, TypeScript, Tailwind CSS, Recharts |
| Backend    | FastAPI, Python 3.12, Pydantic v2                       |
| Data       | SQLAlchemy 2.0 (typed ORM), Alembic, PostgreSQL 16     |
| Async      | Celery 5.4, Redis 7                                    |
| ML         | scikit-learn, pandas, NumPy, joblib                     |
| Auth       | JWT (python-jose), bcrypt (passlib)                     |
| Infra      | Docker, Docker Compose, Makefile                        |
| Testing    | pytest, ruff                                            |

---

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose

### Setup

```bash
git clone https://github.com/JonatanLiljeblad/Smart_Insight_Dashboard.git
cd Smart_Insight_Dashboard
cp .env.example .env

make up          # build and start all 5 services
make migrate     # run database migrations
make seed        # populate 15 players + 180 stat records
make train       # train ML model and save artifact
```

### Verify

```bash
curl http://localhost:8000/health
# → {"status":"ok"}
```

Open http://localhost:3000, register an account, and explore the dashboard. Click any player to see their stats, trend chart, and generate an ML prediction.

### Stop

```bash
make down
```

---

## API

| Method | Endpoint                     | Auth   | Description                     |
|--------|------------------------------|--------|---------------------------------|
| GET    | `/health`                    | —      | Health check                    |
| POST   | `/api/auth/register`         | —      | Create account                  |
| POST   | `/api/auth/login`            | —      | Get JWT token                   |
| GET    | `/api/auth/me`               | Bearer | Current user                    |
| GET    | `/api/players/`              | Bearer | List players                    |
| GET    | `/api/players/{id}`          | Bearer | Player detail                   |
| GET    | `/api/players/{id}/stats`    | Bearer | Player stat history             |
| GET    | `/api/favorites/`            | Bearer | List favorites                  |
| POST   | `/api/favorites/`            | Bearer | Add favorite                    |
| DELETE | `/api/favorites/{id}`        | Bearer | Remove favorite                 |
| POST   | `/api/predictions/`          | Bearer | Create async prediction job     |
| GET    | `/api/predictions/{id}`      | Bearer | Poll prediction job status      |

Interactive docs at http://localhost:8000/docs

---

## Project Structure

```
├── client/                    # Next.js frontend
│   └── src/
│       ├── app/               # Pages: dashboard, login, register, players, favorites
│       ├── components/        # UI, auth, charts, predictions
│       ├── hooks/             # useAuth, usePlayers, useFavorites, usePrediction
│       ├── services/          # Typed API client layer
│       └── types/             # TypeScript interfaces
│
├── server/                    # FastAPI backend
│   ├── app/
│   │   ├── api/routes/        # Auth, players, favorites, predictions
│   │   ├── api/dependencies/  # Auth middleware
│   │   ├── core/              # Config, security, Celery app
│   │   ├── db/                # Engine, session, DeclarativeBase
│   │   ├── models/            # User, Player, PlayerStat, Favorite, PredictionJob
│   │   ├── schemas/           # Pydantic request/response schemas
│   │   ├── services/          # Auth + prediction business logic
│   │   ├── tasks/             # Celery task definitions
│   │   └── main.py            # FastAPI entrypoint
│   ├── alembic/               # Database migrations
│   ├── scripts/               # Seed data + model training
│   └── tests/                 # pytest suite
│
├── ml/                        # ML artifacts, training code, evaluation
├── docker-compose.yml         # 5-service orchestration
├── Makefile                   # Developer workflow commands
└── .env.example               # Environment variable template
```

---

## Development

| Command             | Description                              |
|---------------------|------------------------------------------|
| `make up`           | Build and start all services             |
| `make down`         | Stop and tear down                       |
| `make logs`         | Tail all service logs                    |
| `make worker-logs`  | Tail Celery worker logs                  |
| `make migrate`      | Apply Alembic migrations                 |
| `make seed`         | Seed demo data                           |
| `make train`        | Train and save ML model                  |
| `make test`         | Run pytest (7 tests)                     |
| `make lint`         | Lint with ruff                           |

---

## Why This Project

This isn't a tutorial app. It's designed to demonstrate how real systems work:

- **Async job processing** — predictions don't block the API. Celery workers process them independently, with Redis as the message broker. The frontend polls for results.
- **ML in production context** — the model isn't a notebook. It's trained from a script, saved as an artifact, loaded by the worker, and served through an API with proper job lifecycle management.
- **Clean separation** — routes don't contain business logic. Models don't leak into schemas. The service layer handles coordination. Each file has one clear responsibility.
- **System design** — 5 services, 3 data stores, async messaging, typed ORM, migration management, environment-based configuration. The kind of architecture you'd see in a real backend team.

---

## Author

**Jonatan Filip Liljeblad**
CS & Math @ Albright College · Data Analytics Minor

[LinkedIn](https://www.linkedin.com/in/jonatan-liljeblad-690344260/) · [GitHub](https://github.com/JonatanLiljeblad)

## License

[MIT](LICENSE)
