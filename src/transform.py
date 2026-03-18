"""
Transform: build dimensional CSVs (companies, locations) and jobs fact from clean data.
"""

import pandas as pd

from io_utils import normalize_column_names
from settings import PipelinePaths, resolve_transform_step_input_csv

MINIMAL_COLUMNS = frozenset({"job_title", "company"})


def _build_companies_dimension(jobs_df: pd.DataFrame) -> pd.DataFrame:
    companies = (
        jobs_df[["company"]]
        .drop_duplicates()
        .reset_index(drop=True)
        .rename(columns={"company": "company_name"})
    )
    companies.insert(0, "company_id", range(1, len(companies) + 1))
    return companies


def _build_locations_dimension(jobs_df: pd.DataFrame) -> pd.DataFrame:
    if "location" in jobs_df.columns:
        locations = (
            jobs_df[["location"]]
            .fillna("")
            .drop_duplicates()
            .reset_index(drop=True)
            .rename(columns={"location": "location_name"})
        )
    else:
        locations = pd.DataFrame({"location_id": [], "location_name": []})

    if not locations.empty:
        locations.insert(0, "location_id", range(1, len(locations) + 1))
    return locations


def _build_jobs_fact(
    jobs_df: pd.DataFrame,
    companies_df: pd.DataFrame,
    locations_df: pd.DataFrame,
) -> pd.DataFrame:
    company_name_to_id = dict(
        zip(companies_df["company_name"], companies_df["company_id"])
    )
    if locations_df.empty:
        location_name_to_id = {}
    else:
        location_name_to_id = dict(
            zip(locations_df["location_name"], locations_df["location_id"])
        )

    fact = pd.DataFrame()
    fact["job_title"] = jobs_df["job_title"]
    fact["company_id"] = jobs_df["company"].map(company_name_to_id)
    if "location" in jobs_df.columns:
        fact["location_id"] = jobs_df["location"].map(
            lambda name: location_name_to_id.get(name, pd.NA)
        )
    else:
        fact["location_id"] = pd.NA
    fact["description"] = (
        jobs_df["description"] if "description" in jobs_df.columns else ""
    )
    fact = fact.reset_index(drop=True)
    fact.insert(0, "job_id", range(1, len(fact) + 1))
    return fact


def run_transform() -> None:
    """Read cleaned jobs, emit companies / locations / jobs CSVs for load."""
    input_path = resolve_transform_step_input_csv()
    if not input_path.exists():
        raise FileNotFoundError(
            f"Cleaned input not found: {input_path}. Run src/clean.py first."
        )

    jobs_df = pd.read_csv(input_path)
    normalize_column_names(jobs_df)

    if not MINIMAL_COLUMNS.issubset(jobs_df.columns):
        raise ValueError(
            "Input must contain at least 'job_title' and 'company' columns"
        )

    companies_df = _build_companies_dimension(jobs_df)
    locations_df = _build_locations_dimension(jobs_df)
    jobs_fact_df = _build_jobs_fact(jobs_df, companies_df, locations_df)

    out_dir = PipelinePaths.BLOB_PROCESSED_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    companies_df.to_csv(PipelinePaths.COMPANIES_CSV, index=False)
    locations_df.to_csv(PipelinePaths.LOCATIONS_CSV, index=False)
    jobs_fact_df.to_csv(PipelinePaths.JOBS_CSV, index=False)

    print(
        f"Wrote {len(companies_df)} companies, {len(locations_df)} locations, "
        f"{len(jobs_fact_df)} jobs to {out_dir}"
    )


def main() -> None:
    run_transform()


if __name__ == "__main__":
    main()
