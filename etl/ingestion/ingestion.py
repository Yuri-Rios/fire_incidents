"""
Extracts Fire Incidents from public API and stores the data as JSON files
in the storage/bronze/raw_api folder.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
import requests

ENDPOINT = 'https://data.sfgov.org/resource/wr8u-xric.json'
OUTPUT_SUBDIR = 'storage/ingestion'


def fetch_api_data(url, params=None, headers=None, output_subdir: str = None):
    """Fetch data from API and save to JSON file."""
    try:
        print('Start fetching data...')

        # Resolve project root and output directory
        project_root = Path(__file__).resolve().parents[2]
        output_dir = project_root / output_subdir
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Output directory: {output_dir}")

        # Make the request
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()

        try:
            data = response.json()
        except ValueError:
            print("ERROR: Response content is not valid JSON.")
            return

        if not isinstance(data, list) or not data:
            print("WARNING: Received empty or unexpected JSON structure.")
            return

        print(f"Fetched {len(data)} records.")

        # Prepare output file path with timestamp
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        output_path = output_dir / f"fire_incidents_landing_{timestamp}.json"

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as e:
            print(f"ERROR writing file: {e}")
            return

        print(f"Data saved successfully to: {output_path}")

    except requests.exceptions.RequestException as e:
        print(f"ERROR fetching data from API: {e}")

if __name__ == "__main__":
    fetch_api_data(url=ENDPOINT, output_subdir=OUTPUT_SUBDIR)
