# vessel_app/models.py

from django.db import models

class VesselReading(models.Model):
    device_id = models.IntegerField()
    level = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Device {self.device_id}: {self.level} at {self.timestamp}"
