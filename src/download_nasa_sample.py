import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "data" / "landing" / "firms"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

map_key = os.environ["FIRMS_MAP_KEY"]

# url = (
#     "https://firms.modaps.eosdis.nasa.gov/"
#     f"api/area/csv/{map_key}/VIIRS_NOAA20_NRT/-125,32,-114,42/1"
# )

url = (
    "https://firms.modaps.eosdis.nasa.gov/"
    f"api/area/csv/{map_key}/VIIRS_NOAA20_SP/"
    "-125,32,-114,42/1/2024-07-01"
)

response = requests.get(url, timeout=60)
response.raise_for_status()

output_file = OUTPUT_DIR / "firms_sample.csv"
output_file.write_bytes(response.content)

print(f"Saved {output_file}")