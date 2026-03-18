"""
Clean: normalize text, drop invalid rows, deduplicate; write cleaned jobs CSV.
"""

import pandas as pd

from io_utils import normalize_column_names, normalize_string_columns
from settings import PipelinePaths, resolve_clean_step_input_csv

MINIMAL_COLUMNS = frozenset({"job_title", "company"})


def run_clean() -> None:
    """Load raw landing (or legacy), clean, write processed clean_jobs.csv."""
    input_path = resolve_clean_step_input_csv()
    if not input_path.exists():
        raise FileNotFoundError(f"Ingested file not found: {input_path}")

    jobs_df = pd.read_csv(input_path)
    normalize_column_names(jobs_df)

    if not MINIMAL_COLUMNS.issubset(jobs_df.columns):
        raise ValueError(
            "Input must contain at least 'job_title' and 'company' columns"
        )

    normalize_string_columns(jobs_df)

    jobs_df = jobs_df[
        ~((jobs_df["job_title"] == "") | (jobs_df["company"] == ""))
    ]
    jobs_df = jobs_df.drop_duplicates()

    output_path = PipelinePaths.CLEAN_JOBS_CSV
    output_path.parent.mkdir(parents=True, exist_ok=True)
    jobs_df.to_csv(output_path, index=False)

    print(f"Cleaned {len(jobs_df)} records -> {output_path}")


def main() -> None:
    run_clean()


if __name__ == "__main__":
    main()
