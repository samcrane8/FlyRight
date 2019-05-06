from django.contrib.gis.db import models
from users.models import IcarusUser as User
from icarus_backend.drone.DroneModel import Drone
from icarus_backend.flight.FlightModel import Flight


class Asset(models.Model):
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE)
    flight = models.ForeignKey('Flight', on_delete=models.CASCADE)
    operator = models.ForeignKey(User, on_delete=models.CASCADE)

    def as_dict(self):
        return {
            "drone_id": self.drone.id,
            "flight_id": self.flight.id,
            "operator_id": self.operator.id
        }

    class Meta:
        unique_together = (('drone', 'flight'),)
