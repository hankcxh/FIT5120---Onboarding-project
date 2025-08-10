from django.db import models

# Create your models here.


class ParkingZone(models.Model):
    zone_number = models.CharField(max_length=32, unique=True)
    street_name = models.CharField(max_length=255, blank=True, null=True)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    total_spots = models.IntegerField(null=True, blank=True)
    available_spots = models.IntegerField(null=True, blank=True)
    latest_update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.zone_number} - {self.street_name or ''}"
