"""
End-to-end pipeline orchestrator.

Runs all steps: ingest -> clean -> transform -> load
"""

import sys
from pathlib import Path

# Add src to path to import modules
sys.path.insert(0, str(Path(__file__).parent))

from ingest import main as ingest_main
from clean import main as clean_main
from transform import main as transform_main
from load import main as load_main


def main():
    print("=" * 60)
    print("JOB MARKET DATA PIPELINE")
    print("=" * 60)

    try:
        print("\n[1/4] Running ingest...")
        ingest_main()

        print("\n[2/4] Running clean...")
        clean_main()

        print("\n[3/4] Running transform...")
        transform_main()

        print("\n[4/4] Running load...")
        load_main()

        print("\n" + "=" * 60)
        print("✅ PIPELINE COMPLETE")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ PIPELINE FAILED: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
