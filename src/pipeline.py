"""
Orchestrate the full pipeline: ingest → clean → transform → load.

Run from repository root:
    python src/pipeline.py
"""

import sys

from clean import run_clean
from ingest import run_ingest
from load import run_load
from transform import run_transform

STEP_RUNNERS = (
    ("ingest", run_ingest),
    ("clean", run_clean),
    ("transform", run_transform),
    ("load", run_load),
)


def run_pipeline() -> None:
    print("=" * 60)
    print("JOB MARKET DATA PIPELINE")
    print("=" * 60)

    try:
        for index, (step_name, runner) in enumerate(STEP_RUNNERS, start=1):
            print(f"\n[{index}/4] Running {step_name}...")
            runner()

        print("\n" + "=" * 60)
        print("PIPELINE COMPLETE")
        print("=" * 60)
    except Exception as exc:
        print(f"\nPIPELINE FAILED: {exc}")
        sys.exit(1)


def main() -> None:
    run_pipeline()


if __name__ == "__main__":
    main()
