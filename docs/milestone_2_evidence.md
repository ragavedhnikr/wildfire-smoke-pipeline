# Milestone 2 evidence - Bronze ingestion

## Databricks tables

| Table | Expected rows | Actual rows | Metadata complete | Duplicate check |
|---|---:|---:|---|---|
| `main.wildfire_smoke.bronze_firms_raw` | 99 |  |  |  |
| `main.wildfire_smoke.bronze_aqs_pm25_raw` | 8068 |  |  |  |
| `main.wildfire_smoke.bronze_noaa_raw` | 27259 |  |  |  |
| `main.wildfire_smoke.bronze_noaa_station_metadata_raw` | 3238 |  |  |  |

## Manifest

- [ ] `bronze_ingest_manifest` exists.
- [ ] Each file has a SHA-256 hash.
- [ ] Each successful batch has a batch ID.
- [ ] Reingesting the same hash is skipped.

## Verification queries

Use the queries in the project handoff instructions and paste the results here.
