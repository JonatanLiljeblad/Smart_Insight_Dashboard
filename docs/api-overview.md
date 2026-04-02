# API Overview

## Auth
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/auth/signup` | Register a new user |
| POST | `/api/auth/login` | Log in and receive JWT |

## Users
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/users/me` | Get current authenticated user |

## Data
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/data/player/{id}/stats` | Get player statistics |
