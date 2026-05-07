# Jobs4Hire — Backend API

REST API for the Jobs4Hire developer marketplace. Built with **Python 3.12 + FastAPI**.

## Quick Start

```bash
# Start PostgreSQL + Redis
docker compose up db redis -d

# Install dependencies
pip install -e ".[dev]"

# Run migrations
alembic upgrade head

# Start dev server
uvicorn app.main:app --reload

# API docs at http://localhost:8000/api/v1/docs
```

## Stack

- **FastAPI** — async REST API
- **PostgreSQL 16** — database with full-text search
- **SQLAlchemy 2.x** — async ORM
- **Alembic** — migrations
- **WorkOS AuthKit** — authentication (GitHub + LinkedIn OAuth)
- **Polar.sh** — payments
- **Redis** — caching + rate limiting

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/developers` | List/search developers |
| GET | `/api/v1/developers/{id}` | Get developer profile |
| POST | `/api/v1/developers` | Create developer profile |
| PATCH | `/api/v1/developers/{id}` | Update profile |
| GET | `/api/v1/jobs` | List/search jobs |
| GET | `/api/v1/jobs/{id}` | Get job details |
| POST | `/api/v1/jobs` | Post a job |
| PATCH | `/api/v1/jobs/{id}` | Update job |
| DELETE | `/api/v1/jobs/{id}` | Close job |
| GET | `/api/v1/companies` | List companies |
| POST | `/api/v1/companies` | Register company |
| PATCH | `/api/v1/companies/{id}` | Update company |
