import pandas as pd
from pathlib import Path

IN_PATH = Path("data/processed/clean_jobs.csv")
OUT_DIR = Path("data/processed")


def main():
    if not IN_PATH.exists():
        raise FileNotFoundError(f"Cleaned input not found: {IN_PATH}. Run src/clean.py first.")

    df = pd.read_csv(IN_PATH)

    # normalize column names to expected names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # ensure expected columns exist
    if "job_title" not in df.columns or "company" not in df.columns:
        raise ValueError("Input must contain at least 'job_title' and 'company' columns")

    # create companies table
    companies = (
        df[["company"]]
        .drop_duplicates()
        .reset_index(drop=True)
        .rename(columns={"company": "company_name"})
    )
    companies.insert(0, "company_id", range(1, len(companies) + 1))

    # create locations table (if location column exists)
    if "location" in df.columns:
        locations = (
            df[["location"]]
            .fillna("")
            .drop_duplicates()
            .reset_index(drop=True)
            .rename(columns={"location": "location_name"})
        )
    else:
        locations = pd.DataFrame({"location_id": [], "location_name": []})

    if not locations.empty:
        locations.insert(0, "location_id", range(1, len(locations) + 1))

    # map company and location ids into jobs
    comp_map = dict(zip(companies["company_name"], companies["company_id"]))
    if not locations.empty:
        loc_map = dict(zip(locations["location_name"], locations["location_id"]))
    else:
        loc_map = {}

    jobs = pd.DataFrame()
    jobs["job_title"] = df["job_title"]
    jobs["company_id"] = df["company"].map(comp_map)
    if "location" in df.columns:
        jobs["location_id"] = df["location"].map(lambda x: loc_map.get(x, pd.NA))
    else:
        jobs["location_id"] = pd.NA
    jobs["description"] = df["description"] if "description" in df.columns else ""

    jobs = jobs.reset_index(drop=True)
    jobs.insert(0, "job_id", range(1, len(jobs) + 1))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    companies.to_csv(OUT_DIR / "companies.csv", index=False)
    locations.to_csv(OUT_DIR / "locations.csv", index=False)
    jobs.to_csv(OUT_DIR / "jobs.csv", index=False)

    print(f"Wrote {len(companies)} companies, {len(locations)} locations, {len(jobs)} jobs to {OUT_DIR}")


if __name__ == "__main__":
    main()
