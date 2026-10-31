from pathlib import Path
import geopandas as gpd

# Define directories relative to script location
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOWNLOADS_DIR = PROJECT_ROOT / "data" / "reference" / "counties" / "tl_2026_us_county"
OUTPUT_DIR = PROJECT_ROOT / "data" / "reference" / "counties" / "generated_shapefile"

# Ensure target directories exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. Load the unzipped national shapefile from your paths
shapefile_path = DOWNLOADS_DIR / "tl_2026_us_county.shp"
us_counties = gpd.read_file(shapefile_path)

# 2. Filter rows where STATEFP (State FIPS code) matches '06' (California)
ca_counties = us_counties[us_counties["STATEFP"] == "06"]

# 3. Save it out as a separate, localized California-only shapefile in your output dir
output_file = OUTPUT_DIR / "ca_counties.shp"
ca_counties.to_file(output_file)

print(f"Successfully extracted {len(ca_counties)} California counties to: {output_file}")
