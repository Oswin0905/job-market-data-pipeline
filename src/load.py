import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("data/job_market.db")
SCHEMA_PATH = Path("sql/schema.sql")
DATA_DIR = Path("data/processed")


def main():
    # paths to CSV files
    companies_csv = DATA_DIR / "companies.csv"
    locations_csv = DATA_DIR / "locations.csv"
    jobs_csv = DATA_DIR / "jobs.csv"

    # check all inputs exist
    for path in [companies_csv, locations_csv, jobs_csv, SCHEMA_PATH]:
        if not path.exists():
            raise FileNotFoundError(f"Required file not found: {path}. Run src/transform.py first.")

    # create/connect to database
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    # execute schema
    with open(SCHEMA_PATH, "r") as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)

    # load companies
    companies_df = pd.read_csv(companies_csv)
    companies_df.to_sql("companies", conn, if_exists="append", index=False)

    # load locations
    locations_df = pd.read_csv(locations_csv)
    locations_df.to_sql("locations", conn, if_exists="append", index=False)

    # load jobs
    jobs_df = pd.read_csv(jobs_csv)
    jobs_df.to_sql("jobs", conn, if_exists="append", index=False)

    conn.commit()
    conn.close()

    print(f"Loaded {len(companies_df)} companies, {len(locations_df)} locations, {len(jobs_df)} jobs into {DB_PATH}")


if __name__ == "__main__":
    main()
