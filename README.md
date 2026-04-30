# Smart Insights Dashboard
> ⚡ Built to demonstrate production-style backend systems, async processing, and ML integration — not just a CRUD app.

Full-stack analytics platform for tracking professional golf performance and generating machine learning–based scoring predictions.

Designed as a production-style system with an async job pipeline (Celery + Redis), typed API (FastAPI + SQLAlchemy), and a modern frontend (Next.js), all orchestrated across five Docker services.

![Dashboard](docs/screenshots/dashboard.png)

---

## Demo

```bash
make up && make migrate && make seed && make train
```

| Service         | URL                         |
|-----------------|-----------------------------|
| Dashboard       | http://localhost:3000        |
| API             | http://localhost:8000        |
| Interactive Docs| http://localhost:8000/docs   |

![Player Detail](docs/screenshots/player-detail.png)

---

## 💡 Why This Project?

This project goes beyond CRUD applications and focuses on real-world backend challenges:

- Designing async job pipelines to handle long-running ML tasks
- Integrating machine learning into a production-style system
- Building a clean separation between API, worker, and data layers
- Managing stateful workflows (job lifecycle, polling, result persistence)

It reflects how modern data-driven applications are built in production environments.

---

## Key Features

### Data & Analytics
- Historical stat tracking across 5 performance dimensions per player
- Trend visualization (scoring average, strokes gained, driving accuracy, GIR, putting)
- Per-user favorites with dashboard-level aggregation
- Real stat cards computed from actual data — no hardcoded values

### Machine Learning
- Predicts next scoring average using rolling-window feature engineering over recent performances
- Evaluated baseline (Linear Regression) vs ensemble model (Random Forest)
- Trained artifact served through async job pipeline — predictions never block the API
- Full job lifecycle: `pending → running → completed | failed` with error handling

### Async Processing
- Celery worker consumes jobs from Redis, runs inference, writes results to Postgres
- Frontend polls job status and renders prediction on completion
- Worker and API share the same codebase but run as independent containerized services

### Authentication
- JWT auth with bcrypt hashing, Bearer token scheme
- Protected routes across both API and frontend

---

## Architecture

```
┌────────────┐     ┌────────────┐     ┌────────────┐
│   Next.js  │────▶│  FastAPI   │────▶│ PostgreSQL │
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

| Service    | Role                              |
|------------|-----------------------------------|
| `client`   | Next.js 15 frontend (SSR + SPA)   |
| `server`   | FastAPI REST API + auth           |
| `worker`   | Celery task processor             |
| `db`       | PostgreSQL 16, persistent volume  |
| `redis`    | Message broker + result backend   |

**Prediction request flow:**
1. `POST /api/predictions/` creates a `PredictionJob` record
2. Celery task dispatched to worker via Redis
3. Worker loads model artifact, builds feature vector from recent stats, runs inference
4. Result written to DB → client polls `GET /api/predictions/{id}` until complete

---

## ⚙️ System Design Highlights

- **Non-blocking inference** — predictions run asynchronously via Celery workers
- **Event-driven workflow** — job creation, execution, and completion handled via Redis queue
- **Stateless API layer** — FastAPI handles requests while heavy computation is offloaded
- **Scalable by design** — worker processes can be horizontally scaled independently

---

## ML Pipeline

```
Historical Stats → Feature Engineering → Model Training → Saved Artifact
                                                              │
Player Request → Recent Stats → Feature Vector → Inference → Result
```

| Detail            | Value                                       |
|-------------------|---------------------------------------------|
| Task              | Predict next scoring average                |
| Features          | 3-event rolling mean across 5 stat columns  |
| Baseline          | LinearRegression — RMSE 0.6264              |
| Improved          | RandomForest — RMSE 0.6211                  |
| Training set      | 135 samples from 15 players × 12 events     |
| Artifact          | `scoring_model.joblib`                      |

---

## Tech Stack

| Layer      | Technologies                                            |
|------------|---------------------------------------------------------|
| Frontend   | Next.js 15, React 19, TypeScript, Tailwind CSS, Recharts|
| Backend    | FastAPI, Python 3.12, Pydantic v2                       |
| Data       | SQLAlchemy 2.0 (typed ORM), Alembic, PostgreSQL 16      |
| Async      | Celery 5.4, Redis 7                                     |
| ML         | scikit-learn, pandas, NumPy, joblib                     |
| Auth       | JWT (python-jose), bcrypt (passlib)                     |
| Infra      | Docker, Docker Compose, Makefile                        |
| Quality    | pytest, ruff                                            |

---

## Getting Started

**Requires:** [Docker](https://docs.docker.com/get-docker/) and Docker Compose

```bash
git clone https://github.com/JonatanLiljeblad/Smart_Insight_Dashboard.git
cd Smart_Insight_Dashboard
cp .env.example .env

make up          # build and start all 5 services
make migrate     # apply Alembic migrations
make seed        # load 15 players + 180 stat records
make train       # train and save ML model artifact
```

```bash
curl http://localhost:8000/health
# → {"status":"ok"}
```

Open http://localhost:3000 → register → explore the dashboard → click a player → generate a prediction.

```bash
make down        # stop and tear down
```

---

## API

| Method | Endpoint                     | Auth   | Description                     |
|--------|------------------------------|--------|---------------------------------|
| GET    | `/health`                    | —      | Health check                    |
| POST   | `/api/auth/register`         | —      | Create account                  |
| POST   | `/api/auth/login`            | —      | Get access token + set refresh cookie |
| POST   | `/api/auth/refresh`          | Cookie | Rotate refresh cookie + issue new access token |
| POST   | `/api/auth/logout`           | Cookie | Revoke current refresh session  |
| GET    | `/api/auth/me`               | Bearer | Current user                    |
| GET    | `/api/players/`              | Public | List players                    |
| GET    | `/api/players/{id}`          | Public | Player detail                   |
| GET    | `/api/players/{id}/stats`    | Public | Stat history                    |
| GET    | `/api/favorites/`            | Bearer | List favorites                  |
| POST   | `/api/favorites/`            | Bearer | Add favorite                    |
| DELETE | `/api/favorites/{id}`        | Bearer | Remove favorite                 |
| POST   | `/api/predictions/`          | Bearer | Create prediction job (async)   |
| GET    | `/api/predictions/{id}`      | Bearer | Poll job status + result        |

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
│   ├── scripts/               # Seed data, model training
│   └── tests/                 # pytest suite
│
├── ml/                        # Artifacts, evaluation metrics
├── docker-compose.yml         # 5-service orchestration
├── Makefile                   # Developer workflow
└── .env.example               # Environment template
```

---

## Development

| Command             | Description                              |
|---------------------|------------------------------------------|
| `make up`           | Build and start all services             |
| `make down`         | Stop and tear down                       |
| `make logs`         | Tail all service logs                    |
| `make worker-logs`  | Tail Celery worker logs                  |
| `make migrate`      | Apply database migrations                |
| `make seed`         | Seed demo data                           |
| `make train`        | Train and save ML model                  |
| `make test`         | Run pytest suite                         |
| `make lint`         | Lint with ruff                           |

---

## Design Decisions

- **Async over sync** — predictions dispatch to Celery rather than running in the request cycle. The API stays responsive regardless of model complexity or load.
- **ML as a service** — the model is trained offline, saved as an artifact, and loaded by the worker at task time. Swapping models requires no code changes to the API.
- **Separation of concerns** — routes delegate to services, services operate on models, schemas define the API contract. No ORM leakage into route handlers.
- **Public catalog, protected user actions** — player and stat reads stay public for product discoverability, while favorites, identity, and prediction jobs remain authenticated and abuse-resistant.
- **Shared image, separate roles** — the API server and Celery worker use the same Docker image with different entrypoints, keeping the deployment surface small.

---

## 🔭 Future Improvements

- Replace polling with WebSockets for real-time job updates
- Add model versioning and experiment tracking (MLflow)
- Introduce caching layer for frequently accessed player data
- Deploy to cloud infrastructure (AWS/GCP) with CI/CD pipeline

---

## Author

**Jonatan Filip Liljeblad**
CS & Math @ Albright College · Data Analytics Minor

[LinkedIn](https://www.linkedin.com/in/jonatan-liljeblad-690344260/) · [GitHub](https://github.com/JonatanLiljeblad)

## License

[MIT](LICENSE)
