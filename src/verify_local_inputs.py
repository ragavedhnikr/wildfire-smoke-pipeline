"""Validate local sample files before uploading them to Databricks."""

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LANDING = ROOT / "data" / "landing"


def check_csv(path: Path) -> None:
    with path.open(newline="") as stream:
        rows = list(csv.reader(stream))
    if not rows:
        raise ValueError(f"Empty CSV: {path}")
    print(f"{path.name}: {max(0, len(rows) - 1)} data rows, {len(rows[0])} columns")
    print(f"  columns: {', '.join(rows[0])}")


def check_json(path: Path, collection_key: str) -> None:
    body = json.loads(path.read_text())
    records = body.get(collection_key, [])
    if not isinstance(records, list):
        raise ValueError(f"{path} does not contain a list at '{collection_key}'")
    print(f"{path.name}: {len(records)} records")
    if records:
        print(f"  fields: {', '.join(records[0].keys())}")


def main() -> None:
    check_csv(LANDING / "firms" / "firms_sample.csv")
    check_json(LANDING / "aqs" / "aqs_pm25_sample.json", "Data")
    check_json(LANDING / "noaa" / "noaa_weather_sample.json", "results")
    check_json(LANDING / "noaa" / "noaa_station_metadata.json", "results")

    county_file = (
        ROOT / "data" / "reference" / "counties" / "generated_shapefile" / "ca_counties.shp"
    )
    print(f"California county shapefile: {'present' if county_file.exists() else 'missing'}")


if __name__ == "__main__":
    main()
