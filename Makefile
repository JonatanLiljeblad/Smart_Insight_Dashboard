.PHONY: up down logs test test-server build-client lint lint-server seed migrate train worker-logs

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
	$(MAKE) test-server
	$(MAKE) build-client

test-server:
	docker compose exec server pytest -q

build-client:
	docker compose exec client npm run build

# ── Linting ────────────────────────────────────────────
lint:
	$(MAKE) lint-server

lint-server:
	docker compose exec server ruff check .
