# Data contract

## Common metadata

Every Bronze table must include:

- `_source_system`
- `_source_uri`
- `_source_file_name`
- `_source_file_sha256`
- `_ingest_batch_id`
- `_ingested_at_utc`
- `_schema_version`
- `_record_hash`

## Bronze source columns

### NASA FIRMS

`latitude`, `longitude`, `bright_ti4`, `scan`, `track`, `acq_date`, `acq_time`, `satellite`, `instrument`, `confidence`, `version`, `bright_ti5`, `frp`, `daynight`, `type`

### EPA AQS PM2.5

`state_code`, `county_code`, `site_number`, `parameter_code`, `poc`, `latitude`, `longitude`, `date_local`, `units_of_measure`, `sample_duration_code`, `sample_duration`, `arithmetic_mean`, `first_max_value`, `first_max_hour`, `aqi`, `method_code`, `method`, `validity_indicator`, `state`, `county`, `city`, `date_of_last_change`

### NOAA GHCND

Observation response: `station`, `date`, `datatype`, `value`, `attributes`

Station metadata response: `id`, `name`, `latitude`, `longitude`, `elevation`, `mindate`, `maxdate`

## Silver normalized columns

- NASA: `event_date_local`, `event_ts_utc`, `county_fips`
- EPA: `site_num`, `event_date_local`, `county_fips`
- NOAA: `station_id`, `date_local`, `station_name`, `county_fips`

## Silver common keys

- `county_fips`
- `event_date_local`
- `geography_match_status`
- `validation_status`
