# F1 2026 Data API

FastAPI backend for F1 telemetry and timing data using fastf1 and Neon PostgreSQL.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file:
   ```env
   DATABASE_URL=postgresql+asyncpg://user:pass@host/dbname
   FASTF1_CACHE_DIR=./fastf1_cache
   SYNC_TOKEN=your-secret-token
   ```

4. Run Alembic migrations:
   ```bash
   alembic upgrade head
   ```

5. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Seed 2026 Data

```bash
python scripts/seed_2026.py
```

## Sync a Single Race

```bash
python scripts/sync_race.py 2026 1
```

## API Endpoints

- `GET /health` — Health check
- `GET /races` — List races
- `GET /races/{race_id}` — Race details
- `GET /drivers` — List drivers
- `GET /drivers/{driver_id}` — Driver details
- `GET /drivers/{driver_id}/telemetry` — Driver telemetry
- `GET /sessions/{session_id}` — Session details
- `GET /sessions/{session_id}/laps` — Session laps
- `GET /sessions/{session_id}/telemetry` — Session telemetry
- `GET /sessions/{session_id}/results` — Session results
- `GET /sessions/{session_id}/pitstops` — Session pit stops
- `GET /circuits` — List circuits
- `GET /teams` — List teams
- `POST /sync/races?token=...` — Sync a race (requires `X-Sync-Token` or `token` query param)
- `POST /sync/all?token=...` — Sync all 2026 data
