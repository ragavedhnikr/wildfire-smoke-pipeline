import os
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import requests
from dotenv import load_dotenv

load_dotenv()

FIRMS_MAP_KEY = os.getenv("FIRMS_MAP_KEY")
AQS_EMAIL = os.getenv("AQS_EMAIL")
AQS_KEY = os.getenv("AQS_KEY")
NOAA_TOKEN = os.getenv("NOAA_TOKEN")


def redact_url(url: str) -> str:
    """Remove EPA credentials from a URL before displaying it."""
    parts = urlsplit(url)
    safe_query = []
    for name, value in parse_qsl(parts.query, keep_blank_values=True):
        if name in {"email", "key"}:
            value = "[REDACTED]"
        safe_query.append((name, value))
    return urlunsplit(
        (parts.scheme, parts.netloc, parts.path, urlencode(safe_query), parts.fragment)
    )


def test_firms():
    url = (
        "https://firms.modaps.eosdis.nasa.gov/"
        f"mapserver/mapkey_status/?MAP_KEY={FIRMS_MAP_KEY}"
    )

    response = requests.get(url, timeout=30)
    print("NASA FIRMS:", response.status_code)

    if response.ok:
        body = response.json()
        print("NASA response fields:", list(body.keys()))
    else:
        print(response.text[:300])


def test_aqs():
    url = "https://aqs.epa.gov/data/api/list/countiesByState"

    params = {
        "email": AQS_EMAIL,
        "key": AQS_KEY,
        "state": "06",
    }

    response = requests.get(url, params=params, timeout=30)
    print("EPA AQS:", response.status_code)

    if response.ok:
        body = response.json()
        header = body.get("Header", [{}])
        status = header[0].get("status") if header else None
        print("EPA status:", status)
        print("EPA records:", len(body.get("Data", [])))
    else:
        print("EPA request URL:", redact_url(response.url))
        print("EPA request failed with status:", response.status_code)


def test_noaa():
    url = "https://www.ncei.noaa.gov/cdo-web/api/v2/datasets"

    response = requests.get(
        url,
        headers={"token": NOAA_TOKEN},
        params={"limit": 5},
        timeout=30,
    )

    print("NOAA:", response.status_code)

    if response.ok:
        body = response.json()
        print("NOAA datasets:", len(body.get("results", [])))
    else:
        print(response.text[:300])


if __name__ == "__main__":
    test_firms()
    test_aqs()
    test_noaa()
