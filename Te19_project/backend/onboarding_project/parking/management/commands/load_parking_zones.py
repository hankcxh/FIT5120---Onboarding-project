import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from parking.models import ParkingZone

class Command(BaseCommand):
    help = "Load base zone data from data/melbourne_parking_data.csv"

    def handle(self, *args, **kwargs):
        base = Path(__file__).resolve().parents[3]
        csv_path = base / "data" / "melbourne_parking_data.csv"
        if not csv_path.exists():
            self.stderr.write(f"CSV not found: {csv_path}")
            return

        def f2float(x):
            try: return float(x)
            except: return None
        def f2int(x):
            try: return int(float(x))
            except: return None

        loaded = 0
        with csv_path.open(newline="", encoding="utf-8") as f:
            r = csv.DictReader(f)
            for row in r:
                zone = (row.get("parking_zone") or "").strip()
                if not zone:
                    continue
                ParkingZone.objects.update_or_create(
                    zone_number=zone,
                    defaults={
                        "street_name": row.get("street_name") or None,
                        "lat": f2float(row.get("lat")),
                        "lon": f2float(row.get("lon")),
                        "total_spots": f2int(row.get("total_spots")),
                        "available_spots": f2int(row.get("available_spots")),
                    },
                )
                loaded += 1
        self.stdout.write(self.style.SUCCESS(f"Loaded/updated {loaded} zones"))
