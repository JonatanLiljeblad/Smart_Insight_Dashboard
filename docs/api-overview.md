# API Overview

## Access policy

- **Public-read catalog:** players and historical stats
- **Authenticated user actions:** current user, favorites, and prediction jobs
- **Session model:** short-lived Bearer access token plus rotating refresh token stored in an HttpOnly cookie

## Auth

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/auth/register` | Public | Register a new user |
| POST | `/api/auth/login` | Public | Issue an access token and set a refresh cookie |
| POST | `/api/auth/refresh` | Refresh cookie | Rotate the refresh session and return a new access token |
| POST | `/api/auth/logout` | Refresh cookie | Revoke the current refresh session |
| GET | `/api/auth/me` | Bearer | Get the current authenticated user |

## Players

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/players/` | Public | List players |
| GET | `/api/players/{id}` | Public | Get player details |
| GET | `/api/players/{id}/stats` | Public | Get historical stat records |

## Favorites

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/favorites/` | Bearer | List the current user's favorites |
| POST | `/api/favorites/` | Bearer | Add a player to favorites |
| DELETE | `/api/favorites/{id}` | Bearer | Remove a favorite |

## Predictions

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/predictions/` | Bearer | Create a prediction job |
| GET | `/api/predictions/{id}` | Bearer | Fetch job status and result |
