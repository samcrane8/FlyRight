from django.contrib.gis.db import models
from users.models import IcarusUser as User
from django.utils import timezone


class AirspaceRestriction(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    is_constant = models.BooleanField(default=False)
    type = models.TextField()
    description = models.TextField()
    area = models.PolygonField(default='POLYGON EMPTY')

    def as_geojson(self):
        return {
            "type": "FeatureCollection",
            "features": [
                {
                    "geometry": {
                        "coordinates": self.area[0].coords,
                        "type": "Polygon"
                    }
                }
            ]
        }

    def as_dict(self):
        return {
            "created_by": self.created_by.id,
            "starts_at": self.starts_at.isoformat(),
            "ends_at": self.ends_at.isoformat(),
            "is_constant": self.is_constant,
            "type": self.type,
            "description": self.description,
            "area": self.as_geojson()
        }
