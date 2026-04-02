.PHONY: up down logs test lint

# ── Docker ─────────────────────────────────────────────
up:
	docker compose up --build -d

down:
	docker compose down -v

logs:
	docker compose logs -f

# ── Testing ────────────────────────────────────────────
test:
	cd server && pytest -q

# ── Linting ────────────────────────────────────────────
lint:
	cd server && ruff check .
