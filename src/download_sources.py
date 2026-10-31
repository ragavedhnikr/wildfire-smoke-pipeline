"""Placeholder for local source download functions.

Keep credentials in .env and write immutable responses under data/landing.
"""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LANDING_ROOT = PROJECT_ROOT / "data" / "landing"


def main() -> None:
    print(f"Landing directory: {LANDING_ROOT}")
    print("Add NASA, EPA, and NOAA download calls after API smoke tests pass.")


if __name__ == "__main__":
    main()
