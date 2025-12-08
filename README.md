# TWSE Open Data Fetcher
This repository downloads the TWSE open data feed at `t187ap04_L` and saves it as a UTF-8 CSV file.

## Usage
Run the fetch script with Python to download the latest dataset and write it to `data/t187ap04_L.csv`:
```bash
python fetch_t187ap04_L.py
```
If you already have a downloaded JSON file (for example from the Flat workflow), convert it to CSV with:
```bash
python fetch_t187ap04_L.py --input data/t187ap04_L.json --output data/t187ap04_L.csv
```

## Automated updates (Flat Data)
The repository includes a GitHub Actions workflow (`.github/workflows/flat.yml`) that uses the Flat Data action to:
- fetch `https://openapi.twse.com.tw/v1/opendata/t187ap04_L` every 30 minutes (and on pushes/dispatches)
- save the raw payload to `data/t187ap04_L.json`
- regenerate the CSV via the Python converter
