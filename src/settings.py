"""
Pipeline paths and file resolution.

All filesystem locations for inputs, intermediate outputs, and the SQLite warehouse
live here so steps stay free of hardcoded paths. Layout under ``data/blob/``
mirrors a future object-store layout (e.g. raw / processed / warehouse).
"""

from pathlib import Path

# Repository root (parent of ``src/``)
REPO_ROOT = Path(__file__).resolve().parent.parent


class PipelinePaths:
    """Resolved paths for the job market pipeline."""

    # Staging layout (pipeline-generated; maps conceptually to cloud buckets)
    BLOB_RAW_DIR = REPO_ROOT / "data" / "blob" / "raw"
    BLOB_PROCESSED_DIR = REPO_ROOT / "data" / "blob" / "processed"
    BLOB_WAREHOUSE_DIR = REPO_ROOT / "data" / "blob" / "warehouse"

    # Authoritative raw input (edit here to point at another CSV)
    RAW_SOURCE_JOBS_CSV = REPO_ROOT / "data" / "raw" / "jobs_raw.csv"

    # Intermediate artifacts
    RAW_LANDING_JOBS_CSV = BLOB_RAW_DIR / "jobs_raw.csv"
    CLEAN_JOBS_CSV = BLOB_PROCESSED_DIR / "clean_jobs.csv"
    COMPANIES_CSV = BLOB_PROCESSED_DIR / "companies.csv"
    LOCATIONS_CSV = BLOB_PROCESSED_DIR / "locations.csv"
    JOBS_CSV = BLOB_PROCESSED_DIR / "jobs.csv"

    # Legacy paths (if blob outputs are missing, steps can fall back)
    LEGACY_PROCESSED_RAW_JOBS_CSV = REPO_ROOT / "data" / "processed" / "raw_jobs.csv"
    LEGACY_PROCESSED_CLEAN_JOBS_CSV = REPO_ROOT / "data" / "processed" / "clean_jobs.csv"
    LEGACY_PROCESSED_DIR = REPO_ROOT / "data" / "processed"

    DB_PATH = BLOB_WAREHOUSE_DIR / "job_market.db"
    SCHEMA_PATH = REPO_ROOT / "sql" / "schema.sql"


def resolve_raw_source_csv() -> Path:
    """CSV path for the ingest step (source-of-truth raw file)."""
    return PipelinePaths.RAW_SOURCE_JOBS_CSV


def resolve_clean_step_input_csv() -> Path:
    """Input for clean: prefer post-ingest landing file, else legacy processed copy."""
    if PipelinePaths.RAW_LANDING_JOBS_CSV.exists():
        return PipelinePaths.RAW_LANDING_JOBS_CSV
    return PipelinePaths.LEGACY_PROCESSED_RAW_JOBS_CSV


def resolve_transform_step_input_csv() -> Path:
    """Input for transform: prefer cleaned blob output, else legacy."""
    if PipelinePaths.CLEAN_JOBS_CSV.exists():
        return PipelinePaths.CLEAN_JOBS_CSV
    return PipelinePaths.LEGACY_PROCESSED_CLEAN_JOBS_CSV
