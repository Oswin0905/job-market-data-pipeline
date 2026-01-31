import pandas as pd
from pathlib import Path

IN_PATH = Path("data/processed/raw_jobs.csv")
OUT_PATH = Path("data/processed/clean_jobs.csv")


def main():
    if not IN_PATH.exists():
        raise FileNotFoundError(f"Ingested file not found: {IN_PATH}")

    df = pd.read_csv(IN_PATH)

    # normalize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # required columns check
    if "job_title" not in df.columns or "company" not in df.columns:
        raise ValueError("Input must contain at least 'job_title' and 'company' columns")

    # normalize text columns: fillna -> strip -> lowercase
    for col in df.columns:
        if pd.api.types.is_string_dtype(df[col]) or df[col].dtype == object:
            df[col] = df[col].fillna("").astype(str).str.strip().str.lower()

    # drop rows where job_title or company are empty after normalization
    df = df[~((df["job_title"] == "") | (df["company"] == ""))]

    # remove duplicate rows (exact duplicates)
    df = df.drop_duplicates()

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)

    print(f"Cleaned {len(df)} records -> {OUT_PATH}")


if __name__ == "__main__":
    main()
