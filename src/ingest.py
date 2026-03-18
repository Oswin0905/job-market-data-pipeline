"""
Ingest: validate raw CSV and write a dated landing copy for downstream steps.
"""

import pandas as pd

from settings import PipelinePaths, resolve_raw_source_csv

REQUIRED_COLUMNS = frozenset(
    {"job_title", "company", "location", "description"}
)


def run_ingest() -> None:
    """Read source CSV, validate columns, write to raw landing path."""
    source_path = resolve_raw_source_csv()
    if not source_path.exists():
        raise FileNotFoundError(f"Raw data not found at {source_path}")

    jobs_df = pd.read_csv(source_path)
    missing = REQUIRED_COLUMNS - set(jobs_df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    landing_path = PipelinePaths.RAW_LANDING_JOBS_CSV
    landing_path.parent.mkdir(parents=True, exist_ok=True)
    jobs_df.to_csv(landing_path, index=False)

    print(f"Ingested {len(jobs_df)} records -> {landing_path}")


def main() -> None:
    run_ingest()


if __name__ == "__main__":
    main()
