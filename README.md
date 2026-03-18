# Job Market Data Pipeline

Batch ETL pipeline that turns raw job postings (CSV) into cleaned files, a small dimensional model (companies, locations, jobs), and a SQLite warehouse for SQL analytics.

## What it does

| Step        | Role |
|------------|------|
| **Ingest** | Validate required columns; copy source CSV to a raw landing zone |
| **Clean**  | Normalize headers and text; drop bad rows; deduplicate |
| **Transform** | Build `companies` / `locations` / `jobs` CSVs with surrogate keys |
| **Load**   | Apply SQL schema; clear tables; reload from CSV into SQLite |

Outputs under `data/blob/` mirror a typical **raw → processed → warehouse** layout for a future move to object storage and a cloud database.

## Repository layout

```
job-market-data-pipeline/
├── README.md
├── requirements.txt
├── sql/
│   ├── schema.sql      # DDL for SQLite
│   └── analytics.sql   # example analytics queries
├── data/
│   ├── raw/            # put your source CSV here (default: jobs_raw.csv)
│   ├── processed/      # legacy fallback paths only
│   └── blob/           # pipeline outputs (created on run)
│       ├── raw/
│       ├── processed/
│       └── warehouse/  # job_market.db
└── src/
    ├── settings.py     # paths and input resolution
    ├── io_utils.py     # shared DataFrame helpers
    ├── ingest.py
    ├── clean.py
    ├── transform.py
    ├── load.py
    └── pipeline.py     # runs all steps in order
```

## Prerequisites

- Python 3.9+ recommended
- `pandas` (see `requirements.txt`)

## Setup

```bash
git clone https://github.com/Oswin0905/job-market-data-pipeline.git
cd job-market-data-pipeline
pip install -r requirements.txt
```

Place a CSV at `data/raw/jobs_raw.csv` with at least:

`job_title`, `company`, `location`, `description`

## Run

**Step by step** (from repo root):

```bash
python src/ingest.py
python src/clean.py
python src/transform.py
python src/load.py
```

**End-to-end:**

```bash
python src/pipeline.py
```

## Configuration

Paths live in **`src/settings.py`**:

- **`PipelinePaths.RAW_SOURCE_JOBS_CSV`** — source file for ingest
- **`data/blob/...`** — landing, processed CSVs, and SQLite DB

If blob outputs are missing, **clean** can read legacy `data/processed/raw_jobs.csv`; **transform** can read legacy `data/processed/clean_jobs.csv`; **load** can read legacy dimensional CSVs under `data/processed/`.

## Analytics

After load, query `data/blob/warehouse/job_market.db` or run statements from `sql/analytics.sql`.

## Design notes

- **Idempotent load**: tables are truncated in FK-safe order before each reload so reruns (including full pipeline) do not violate primary/unique keys.
- **Separation of concerns**: each step is one module; shared column logic lives in `io_utils.py`; paths in `settings.py`.

## License / portfolio

Suitable as a portfolio example of a small, readable data engineering workflow. Extend with orchestration (e.g. Airflow, ADF), cloud storage, and a managed database when you outgrow local SQLite.
