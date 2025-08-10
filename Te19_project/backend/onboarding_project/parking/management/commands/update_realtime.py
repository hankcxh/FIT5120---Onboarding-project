# parking/management/commands/update_realtime.py
import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from django.utils.timezone import now
from parking.models import ParkingZone

class Command(BaseCommand):
    help = "Update ParkingZone.available_spots from latest sensor CSV (keeps your totals/coords intact)."

    def handle(self, *args, **kwargs):
        # 1) Find the CSV (put it at: onboarding_project/data/on_street_parking_bay_sensors.csv)
        project_root = Path(__file__).resolve().parents[3]
        sensors_csv = project_root / "data" / "on_street_parking_bay_sensors.csv"
        if not sensors_csv.exists():
            self.stderr.write(f"Missing sensors CSV: {sensors_csv}")
            self.stderr.write("Put your file at: <project>/onboarding_project/data/on_street_parking_bay_sensors.csv")
            return

        # 2) Keep the most recent row per KerbsideID, then aggregate by Zone_Number
        # latest_by_kerb: kerb_id -> (timestamp_iso, status, zone_number)
        latest_by_kerb = {}

        def safe_strip(v):
            return (v or "").strip()

        with sensors_csv.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            # Expected headers include: KerbsideID, Zone_Number, Status_Description, Status_Timestamp
            for row in reader:
                kerb = safe_strip(row.get("KerbsideID"))
                zone = safe_strip(row.get("Zone_Number"))
                status = safe_strip(row.get("Status_Description"))  # e.g., "Unoccupied" or "Present"
                ts = safe_strip(row.get("Status_Timestamp"))        # ISO-like string

                if not kerb or not ts:
                    continue

                # Keep only the latest timestamp per kerb
                prev = latest_by_kerb.get(kerb)
                if prev is None or ts > prev[0]:
                    latest_by_kerb[kerb] = (ts, status, zone)

        # 3) Aggregate availability per zone from the latest kerb statuses
        per_zone = {}  # zone -> dict(available, total, latest_ts)
        for kerb, (ts, status, zone) in latest_by_kerb.items():
            if not zone:
                continue
            bucket = per_zone.setdefault(zone, {"available": 0, "total": 0, "latest_ts": ts})
            bucket["total"] += 1
            if status.lower() == "unoccupied":
                bucket["available"] += 1
            # track the most recent timestamp we saw for that zone
            if ts > bucket["latest_ts"]:
                bucket["latest_ts"] = ts

        # 4) Write results into the DB - only update available_spots + latest_update
        updated = 0
        for zone_number, agg in per_zone.items():
            latest = parse_datetime(agg["latest_ts"]) or now()
            # Update existing zones; create if not found (will lack coords unless you loaded them earlier)
            obj, created = ParkingZone.objects.update_or_create(
                zone_number=str(zone_number),
                defaults={
                    "available_spots": int(agg["available"]),
                    "latest_update": latest,
                    # DO NOT touch total_spots, lat, lon, street_name here (keep your curated data)
                }
            )
            updated += 1

        self.stdout.write(self.style.SUCCESS(f"Updated real-time availability for {updated} zones"))
