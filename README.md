# Smart Insights Dashboard v2

A full-stack analytics platform built with **FastAPI**, **Next.js**, **PostgreSQL**, and **Redis** — containerized with Docker Compose.

> 📌 **Status:** Phase 1 — Foundation (services running, health check live)

---

## Tech Stack

| Layer     | Technology                  |
|-----------|-----------------------------|
| Frontend  | Next.js 15, TypeScript, Tailwind CSS |
| Backend   | FastAPI, Python 3.12        |
| Database  | PostgreSQL 16               |
| Cache     | Redis 7                     |
| Infra     | Docker, Docker Compose      |

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

### 3. Verify

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

### 4. Stop

```bash
make down
# or: docker compose down -v
```

---

## Development

### View logs

```bash
make logs
# or: docker compose logs -f
```

### Run backend tests

```bash
make test
# or: docker compose exec server pytest -q
```

### Makefile targets

| Command     | Description                      |
|-------------|----------------------------------|
| `make up`   | Build and start all services     |
| `make down` | Stop and remove all services     |
| `make logs` | Tail logs from all services      |
| `make test` | Run backend test suite           |
| `make lint` | Lint backend with ruff           |

---

## Project Structure

```
├── client/          # Next.js frontend
├── server/          # FastAPI backend
├── data/            # Raw + processed datasets
├── ml/              # ML notebooks, training, artifacts
├── docs/            # Architecture docs, decisions
├── scripts/         # Data loading & seed scripts
├── docker-compose.yml
├── .env.example
├── Makefile
└── README.md
```

---

## Environment Variables

Defined in `.env` (copy from `.env.example`):

| Variable              | Description                        |
|-----------------------|------------------------------------|
| `POSTGRES_DB`         | Database name                      |
| `POSTGRES_USER`       | Database user                      |
| `POSTGRES_PASSWORD`   | Database password                  |
| `DATABASE_URL`        | Full connection string for backend |
| `REDIS_URL`           | Redis connection string            |
| `NEXT_PUBLIC_API_URL` | Backend URL for frontend           |

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
- [ ] Phase 2 — Auth, database models, API routes
- [ ] Phase 3 — Dashboard UI, data visualization
- [ ] Phase 4 — ML integration, predictions
- [ ] Phase 5 — Deployment, CI/CD, polish

---

## Author

**Jonatan Filip Liljeblad**
— CS & Math @ Albright College, Data Analytics minor
— [LinkedIn](https://www.linkedin.com/in/jonatan-liljeblad-690344260/) · [GitHub](https://github.com/JonatanLiljeblad)

## License

[MIT](LICENSE)
