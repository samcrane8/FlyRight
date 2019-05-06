from django.contrib.gis.db import models
from users.models import IcarusUser as User
from django.utils import timezone


class Drone(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    id = models.TextField(primary_key=True)
    description = models.TextField()
    manufacturer = models.TextField()
    type = models.TextField()
    color = models.TextField()
    faa_registration_number = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "owner_id": self.owner.id,
            "description": self.description,
            "manufacturer": self.manufacturer,
            "type": self.type,
            "color": self.color,
            "faa_registration_number": self.faa_registration_number,
            "created_at": self.created_at.isoformat()
        }