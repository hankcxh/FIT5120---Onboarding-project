from django.core.management.base import BaseCommand
from django.core.management import call_command
import time

class Command(BaseCommand):
    help = "Fetch live sensor CSV and update real-time availability. Use --loop N to repeat every N seconds."

    def add_arguments(self, parser):
        parser.add_argument("--loop", type=int, default=0,
                            help="Repeat fetch+update every N seconds (0 = run once)")

    def handle(self, *args, **opts):
        interval = int(opts["loop"])
        if interval <= 0:
            self._run_once()
            return

        self.stdout.write(self.style.WARNING(f"Starting sync loop every {interval}s. Ctrl+C to stop."))
        try:
            while True:
                self._run_once()
                time.sleep(interval)
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("Stopped."))

    def _run_once(self):
        self.stdout.write("Downloading sensors CSV...")
        call_command("fetch_sensors")
        self.stdout.write("Updating real-time availability...")
        call_command("update_realtime")
        self.stdout.write(self.style.SUCCESS("Sync complete."))
