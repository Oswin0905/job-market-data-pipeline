"""
Shared DataFrame helpers used by multiple pipeline steps.

Keeps column-normalization logic in one place so clean and transform stay in sync.
"""

import pandas as pd


def normalize_column_names(df: pd.DataFrame) -> None:
    """Normalize column headers: strip whitespace, lowercase, spaces to underscores."""
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")


def normalize_string_columns(df: pd.DataFrame) -> None:
    """Fill nulls, strip, and lowercase all string/object columns (in place)."""
    for column in df.columns:
        if pd.api.types.is_string_dtype(df[column]) or df[column].dtype == object:
            df[column] = (
                df[column].fillna("").astype(str).str.strip().str.lower()
            )
