"""Seed the database with sample data.

Usage (inside Docker):
    docker compose exec server python -m scripts.seed_data

Usage (outside Docker — requires DATABASE_URL in .env):
    cd server && python -m scripts.seed_data
"""

# The canonical seed script lives at server/scripts/seed_data.py.
# Run it from the server context where app imports are available.

if __name__ == "__main__":
    print("Run this from the server context:")
    print("  docker compose exec server python -m scripts.seed_data")
    print("  — or —")
    print("  make seed")
