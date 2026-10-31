# Access and setup checklist

## Accounts

1. Databricks Free Edition workspace.
2. NASA FIRMS MAP_KEY.
3. EPA AQS email and API key.
4. NOAA CDO token.
5. Optional GitHub repository.

## Local credential setup

Copy `.env.example` to `.env` and fill in the values locally. Never commit `.env`, print the values, or place them in a notebook.

## Smoke tests

Run the API tests from the local terminal before uploading data to Databricks:

```bash
source .venv/bin/activate
set -a
source .env
set +a

curl -fsS "https://firms.modaps.eosdis.nasa.gov/mapserver/mapkey_status/?MAP_KEY=$FIRMS_MAP_KEY"
curl -fsS "https://aqs.epa.gov/data/api/list/countiesByState?email=$AQS_EMAIL&key=$AQS_KEY&state=06"
curl -fsS -H "token: $NOAA_TOKEN" "https://www.ncei.noaa.gov/cdo-web/api/v2/datasets?limit=5"
```

Then validate the downloaded files without printing credentials:

```bash
python src/verify_local_inputs.py
```
