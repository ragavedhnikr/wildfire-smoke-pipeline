# Milestone 1 evidence - feasibility and data contract

## Scope

- Geography: California, state FIPS `06`
- Date range: `2024-07-01` through `2024-07-07`
- NASA sensor/product: `VIIRS_NOAA20_SP`
- EPA parameter: `88101`
- NOAA dataset: `GHCND`
- Time zone policy: preserve source dates and derive California local dates for Silver

## Access tests

| Source | Test command | HTTP status | Result | Date tested |
|---|---|---:|---|---|
| NASA FIRMS | `python src/test_sources.py` |  |  |  |
| EPA AQS | `python src/test_sources.py` |  |  |  |
| NOAA CDO | `python src/test_sources.py` |  |  |  |

## Downloaded samples

| File | Expected records | Actual records | SHA-256 |
|---|---:|---:|---|
| `firms_sample.csv` | 99 |  |  |
| `aqs_pm25_sample.json` | 8068 |  |  |
| `noaa_weather_sample.json` | 27259 |  |  |
| `noaa_station_metadata.json` | 3238 |  |  |

## Contract decisions

- Natural keys are documented in `data_contract.md`.
- EPA credentials are never stored in a source URI or response file.
- Bronze preserves source fields; Silver uses normalized names and units.

## Results from 01_feasiblity.py from Databricks
{'source': 'FIRMS', 'file': 'firms_sample.csv', 'rows': 99, 'sha256': '876355c8a17929380c5ab7c98f22090ad05b818d882d9fdbc1c4215e2b9288dc'}
{'source': 'EPA AQS', 'file': 'aqs_pm25_sample.json', 'rows': 8068, 'sha256': '05252a08f3a26e0cbd117424592e598b7fa3286c172180e2e388b569d1eef0f5'}
{'source': 'NOAA weather', 'file': 'noaa_weather_sample.json', 'rows': 27259, 'sha256': '4c83f323e3fc4c49210fdc9b10df478c535e1f03fade044275d6bfad1d51d38e'}
{'source': 'NOAA stations', 'file': 'noaa_station_metadata.json', 'rows': 3238, 'sha256': '16d7cc6189a36a7d51f3d87e5b001b14f545c3a4d7e9100b07ee0f379ae3efd3'}

## Quality rules
latitude must be between -90 and 90
longitude must be between -180 and 180
required date fields cannot be null
EPA PM2.5 values cannot be negative
NOAA missing values become null
unknown units are quarantined
invalid dates are quarantined
duplicate natural keys use the latest ingestion