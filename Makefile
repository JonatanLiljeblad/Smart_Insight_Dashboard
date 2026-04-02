.PHONY: up down logs test lint seed migrate

# ── Docker ─────────────────────────────────────────────
up:
	docker compose up --build -d

down:
	docker compose down -v

logs:
	docker compose logs -f

# ── Database ───────────────────────────────────────────
migrate:
	docker compose exec server alembic upgrade head

seed:
	docker compose exec server python -m scripts.seed_data

# ── Testing ────────────────────────────────────────────
test:
	cd server && pytest -q

# ── Linting ────────────────────────────────────────────
lint:
	cd server && ruff check .
