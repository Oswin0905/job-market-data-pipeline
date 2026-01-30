import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/jobs_raw.csv")
OUT_PATH = Path("data/processed/raw_jobs.csv")

REQUIRED_COLUMNS = {"job_title", "company", "location", "description"}

def main():
    if not RAW_PATH.exists():
        raise FileNotFoundError(f"Raw data not found at {RAW_PATH}")

    df = pd.read_csv(RAW_PATH)

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)

    print(f"Ingested {len(df)} records")

if __name__ == "__main__":
    main()

