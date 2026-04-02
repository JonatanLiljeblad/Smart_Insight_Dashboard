# Architecture Decision Records

## ADR-001: Monorepo with client/server split
- **Status:** Accepted
- **Context:** Need clear separation between Next.js frontend and FastAPI backend while keeping them in one repo for simpler CI/CD.
- **Decision:** Use a monorepo with `client/` and `server/` top-level directories.
