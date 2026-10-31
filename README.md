# California Wildfire Smoke Data Pipeline

PySpark and Delta Lake project using NASA FIRMS, EPA AQS PM2.5, and NOAA weather data.

## Initial scope

- Geography: California (`state_fips = 06`)
- Grain: county and local calendar day
- Layers: Bronze raw ingestion, Silver cleaning and quality
- Credentials: keep local in `.env`; never commit them

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

See `docs/data_contract.md` and `docs/access_and_setup.md` before downloading data.
