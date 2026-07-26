# F1 Telemetry to Tableau Pipeline

This project extracts Formula 1 telemetry data via FastF1, stores it in SQLite, generates a Tableau Hyper extract, and auto-publishes to a Tableau site via GitHub Actions.

## Pipeline Overview

The pipeline (`scripts/pipeline.py`) runs four phases in sequence:

1. **FastF1 Extraction** — Identifies the latest completed 2026 race using the event schedule, loads session lap data, and caches results under `./data/cache/`.
2. **SQLite** — Writes the extracted lap data to `./data/f1_database.db` in the `LapTimes` table.
3. **Hyper Extract** — Converts the SQLite data into a Tableau Hyper extract saved at `./data/f1_extract.hyper`.
4. **Tableau Publish** — Authenticates with Tableau Server using a personal access token and publishes the Hyper extract to the `Default` project.

## Local Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure the following environment variables are set locally if publishing to Tableau:
   - `TABLEAU_SERVER_URL`
   - `TABLEAU_SITE_ID`
   - `TABLEAU_TOKEN_NAME`
   - `TABLEAU_TOKEN_VALUE`

4. Run the pipeline:
   ```bash
   python scripts/pipeline.py
   ```

## GitHub Actions

The workflow in `.github/workflows/f1_tableau_update.yml` runs:

- On a schedule (every Monday at 12:00 UTC).
- On manual trigger (`workflow_dispatch`).

After publishing, the workflow auto-commits `./data/f1_database.db` back to the repository. The generated `.hyper` file is a derived artifact and is **not** committed.

### Required GitHub Secrets

Configure the following secrets in the repository settings:

| Secret | Description |
|---|---|
| `TABLEAU_SERVER_URL` | URL of your Tableau Server/Cloud site |
| `TABLEAU_SITE_ID` | Site ID for the Tableau site |
| `TABLEAU_TOKEN_NAME` | Name of the Tableau personal access token |
| `TABLEAU_TOKEN_VALUE` | Value of the Tableau personal access token |

## Notes

- FastF1 cache is stored under `./data/cache/`.
- SQLite is the source of truth; the Hyper extract is generated from it each run.
- `.hyper` files are ignored by Git.