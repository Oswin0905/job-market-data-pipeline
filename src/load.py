"""
Load: apply schema, full-refresh dimension and fact tables from CSV into SQLite.
"""

import sqlite3

import pandas as pd

from settings import PipelinePaths


def _resolve_csv_paths():
    """Use blob-processed CSVs, or fall back to legacy data/processed/."""
    companies = PipelinePaths.COMPANIES_CSV
    locations = PipelinePaths.LOCATIONS_CSV
    jobs = PipelinePaths.JOBS_CSV

    if not companies.exists() and PipelinePaths.LEGACY_PROCESSED_DIR.exists():
        legacy = PipelinePaths.LEGACY_PROCESSED_DIR
        companies = legacy / "companies.csv"
        locations = legacy / "locations.csv"
        jobs = legacy / "jobs.csv"

    return companies, locations, jobs


def _clear_loaded_tables(cursor: sqlite3.Cursor) -> None:
    """Delete in FK order so reruns are idempotent."""
    cursor.execute("DELETE FROM jobs;")
    cursor.execute("DELETE FROM companies;")
    cursor.execute("DELETE FROM locations;")


def run_load() -> None:
    """Create DB if needed, apply schema, replace table contents from CSVs."""
    companies_csv, locations_csv, jobs_csv = _resolve_csv_paths()
    schema_path = PipelinePaths.SCHEMA_PATH
    db_path = PipelinePaths.DB_PATH

    for path in (companies_csv, locations_csv, jobs_csv, schema_path):
        if not path.exists():
            raise FileNotFoundError(
                f"Required file not found: {path}. Run src/transform.py first."
            )

    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(db_path))
    cursor = connection.cursor()

    with open(schema_path, "r", encoding="utf-8") as schema_file:
        cursor.executescript(schema_file.read())

    _clear_loaded_tables(cursor)

    companies_df = pd.read_csv(companies_csv)
    companies_df.to_sql("companies", connection, if_exists="append", index=False)

    locations_df = pd.read_csv(locations_csv)
    locations_df.to_sql("locations", connection, if_exists="append", index=False)

    jobs_df = pd.read_csv(jobs_csv)
    jobs_df.to_sql("jobs", connection, if_exists="append", index=False)

    connection.commit()
    connection.close()

    print(
        f"Loaded {len(companies_df)} companies, {len(locations_df)} locations, "
        f"{len(jobs_df)} jobs into {db_path}"
    )


def main() -> None:
    run_load()


if __name__ == "__main__":
    main()
