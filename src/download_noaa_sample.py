"""Download paginated NOAA GHCND observations and station metadata."""

import json
import os
import time
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv


load_dotenv()

NOAA_TOKEN = os.environ["NOAA_TOKEN"]
PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "data" / "landing" / "noaa"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://www.ncei.noaa.gov/cdo-web/api/v2"
PAGE_SIZE = 1_000
REQUEST_DELAY_SECONDS = 0.25


def fetch_all(endpoint: str, params: dict[str, Any]) -> dict[str, Any]:
    """Fetch every page from a NOAA API endpoint."""
    headers = {"token": NOAA_TOKEN}
    results: list[dict[str, Any]] = []
    offset = 1
    total_count: int | None = None

    with requests.Session() as session:
        while True:
            page_params = {
                **params,
                "limit": PAGE_SIZE,
                "offset": offset,
            }

            response = session.get(
                f"{BASE_URL}/{endpoint}",
                headers=headers,
                params=page_params,
                timeout=60,
            )
            response.raise_for_status()
            body = response.json()

            page_results = body.get("results", [])
            resultset = body.get("metadata", {}).get("resultset", {})
            total_count = resultset.get("count", total_count)
            results.extend(page_results)

            print(
                f"{endpoint}: fetched {len(results)}"
                f"/{total_count if total_count is not None else '?'}"
            )

            if not page_results or len(page_results) < PAGE_SIZE:
                break

            offset += len(page_results)
            time.sleep(REQUEST_DELAY_SECONDS)

    return {
        "metadata": {
            "resultset": {
                "count": total_count if total_count is not None else len(results),
                "returned": len(results),
            },
            "query": params,
        },
        "results": results,
    }


def save_json(filename: str, body: dict[str, Any]) -> None:
    output_file = OUTPUT_DIR / filename
    output_file.write_text(json.dumps(body, indent=2))
    print(f"Saved {output_file} ({len(body['results'])} records)")


def main() -> None:
    common_params = {
        "datasetid": "GHCND",
        "locationid": "FIPS:06",
        "startdate": "2024-07-01",
        "enddate": "2024-07-07",
    }

    observations = fetch_all("data", common_params)
    save_json("noaa_weather_sample.json", observations)

    station_params = {
        "datasetid": "GHCND",
        "locationid": "FIPS:06",
    }

    stations = fetch_all("stations", station_params)
    save_json("noaa_station_metadata.json", stations)


if __name__ == "__main__":
    main()
