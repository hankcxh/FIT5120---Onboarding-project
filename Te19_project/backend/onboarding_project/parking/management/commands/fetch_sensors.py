import csv
import io
import time
from pathlib import Path

import requests
from django.conf import settings
from django.core.management.base import BaseCommand

"""
Downloads the City of Melbourne 'On-street parking bay sensors' CSV export,
normalises columns, and writes:
  onboarding_project/data/on_street_parking_bay_sensors.csv

Output columns (for update_realtime):
  KerbsideID, Zone_Number, Status_Description, Status_Timestamp, lat, lon, LastUpdated
"""

EXPORT_URL = (
    "https://data.melbourne.vic.gov.au/api/v2/catalog/datasets/"
    "on-street-parking-bay-sensors/exports/csv"
    "?delimiter=%2C&timezone=Australia%2FMelbourne"
)

HEADERS = {
    "User-Agent": "FIT5120-onboarding-student/1.0",
    "Accept": "text/csv,application/json",
}

# helper to read possibly-varied header names safely
def first_key(row, *candidates):
    for k in candidates:
        if k in row and row[k] not in (None, ""):
            return k
    return None

class Command(BaseCommand):
    help = "Fetch latest sensor data via CSV export and write normalised CSV to ./data/on_street_parking_bay_sensors.csv"

    def handle(self, *args, **kwargs):
        base_dir = Path(settings.BASE_DIR)
        data_dir = base_dir / "data"
        data_dir.mkdir(exist_ok=True)
        out_csv = data_dir / "on_street_parking_bay_sensors.csv"

        # cache-buster so we don't get a CDN-cached copy
        url = f"{EXPORT_URL}&_ts={int(time.time())}"
        self.stdout.write("Downloading CSV export...")
        r = requests.get(url, headers=HEADERS, timeout=60)
        r.raise_for_status()

        raw = r.content.decode("utf-8", errors="replace")
        reader = csv.DictReader(io.StringIO(raw))
        headers = [h for h in (reader.fieldnames or [])]
        if not headers:
            self.stderr.write("No headers returned from export endpoint.")
            return

        self.stdout.write(f"Got CSV with headers: {headers}")

        # Guess header names used by the export (Opendatasoft sometimes changes exact casing)
        # Common ones observed: kerbsideid, zone_number, status_description, status_timestamp,
        # lastupdated, location_lat, location_lon  (or sometimes location.latitude, location.longitude)
        rows_out = []
        for row in reader:
            k_kerb = first_key(row, "kerbsideid", "KerbsideID", "kerbside_id")
            k_zone = first_key(row, "zone_number", "Zone_Number", "zone")
            k_stat_desc = first_key(row, "status_description", "Status_Description", "status")
            k_stat_ts = first_key(row, "status_timestamp", "Status_Timestamp", "status_time", "timestamp")
            k_lastupd = first_key(row, "lastupdated", "LastUpdated", "last_update")

            # lat/lon: export often flattens to 'location_lat'/'location_lon' or 'location.latitude'
            k_lat = first_key(row, "location_lat", "location.latitude", "Latitude", "lat")
            k_lon = first_key(row, "location_lon", "location.longitude", "Longitude", "lon")

            rows_out.append([
                (row.get(k_kerb) or "").strip(),
                (row.get(k_zone) or "").strip(),
                (row.get(k_stat_desc) or "").strip(),
                (row.get(k_stat_ts) or "").strip(),
                (row.get(k_lat) or "").strip() if k_lat else "",
                (row.get(k_lon) or "").strip() if k_lon else "",
                (row.get(k_lastupd) or "").strip(),
            ])

        if not rows_out:
            self.stderr.write("Download succeeded but no data rows were parsed.")
            return

        with out_csv.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["KerbsideID", "Zone_Number", "Status_Description", "Status_Timestamp", "lat", "lon", "LastUpdated"])
            w.writerows(rows_out)

        self.stdout.write(self.style.SUCCESS(f"Saved {len(rows_out)} rows - {out_csv}"))
