"""Download EPA AQS PM2.5 data without persisting credentials."""

import json
import os
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import requests
from dotenv import load_dotenv


load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "data" / "landing" / "aqs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

URL = "https://aqs.epa.gov/data/api/dailyData/byState"


def redact_url(url: str) -> str:
    """Remove AQS credentials from a URL before logging or saving it."""
    parts = urlsplit(url)
    safe_query = []

    for name, value in parse_qsl(parts.query, keep_blank_values=True):
        if name in {"email", "key"}:
            value = "[REDACTED]"
        safe_query.append((name, value))

    return urlunsplit(
        (parts.scheme, parts.netloc, parts.path, urlencode(safe_query), parts.fragment)
    )


def redact_response(payload: dict) -> dict:
    """Redact the URL that EPA echoes inside its response header."""
    header = payload.get("Header")
    if isinstance(header, list):
        for item in header:
            if isinstance(item, dict) and isinstance(item.get("url"), str):
                item["url"] = redact_url(item["url"])
    return payload


def main() -> None:
    # EPA AQS requires email and key as query parameters. They are read from
    # .env and are never hard-coded, printed, or saved in the output file.
    params = {
        "email": os.environ["AQS_EMAIL"],
        "key": os.environ["AQS_KEY"],
        "param": "88101",
        "bdate": "20240701",
        "edate": "20240707",
        "state": "06",
    }

    try:
        response = requests.get(URL, params=params, timeout=60)
        response.raise_for_status()
    except requests.RequestException as exc:
        safe_url = redact_url(getattr(exc.request, "url", URL))
        raise RuntimeError(f"EPA AQS request failed: {safe_url}") from exc

    payload = redact_response(response.json())
    output_file = OUTPUT_DIR / "aqs_pm25_sample.json"
    output_file.write_text(json.dumps(payload, indent=2))

    records = len(payload.get("Data", []))
    print(f"Saved {output_file} ({records} records)")


if __name__ == "__main__":
    main()
