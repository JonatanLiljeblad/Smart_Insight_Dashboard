.PHONY: up down logs test lint seed migrate train worker-logs

# ── Docker ─────────────────────────────────────────────
up:
	docker compose up --build -d

down:
	docker compose down -v

logs:
	docker compose logs -f

worker-logs:
	docker compose logs -f worker

# ── Database ───────────────────────────────────────────
migrate:
	docker compose exec server alembic upgrade head

seed:
	docker compose exec server python -m scripts.seed_data

# ── ML ─────────────────────────────────────────────────
train:
	docker compose exec server python -m scripts.train_model

# ── Testing ────────────────────────────────────────────
test:
	docker compose exec server pytest -q

# ── Linting ────────────────────────────────────────────
lint:
	docker compose exec server ruff check .
