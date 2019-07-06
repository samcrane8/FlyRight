from django.contrib.gis.db import models
from users.models import IcarusUser as User


class Department(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    airbosses = models.ManyToManyField(User, related_name="airboss_profile")
    watchCommanders = models.ManyToManyField(User, related_name="watchcom_profile")
    area = models.PolygonField(default='POLYGON EMPTY')
    name = models.TextField(unique=True)
    # clearance

    def as_geojson(self):
        coords = [[x[0],x[1]] for x in self.area[0].coords]
        return {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "name": self.name
                    },
                    "geometry": {
                        "coordinates": [coords],
                        "type": "Polygon"
                    }
                }
            ]
        }

    def get_airbosses(self):
        return [x.as_dict() for x in self.airbosses.all()]

    def get_watch_commanders(self):
        return [x.as_dict() for x in self.watchCommanders.all()]

    def as_dict(self):
        return {
            "id": self.id,
            "owner": self.owner.as_dict(),
            "name": self.name,
            "area": self.as_geojson(),
            "airbosses": self.get_airbosses(),
            "watch_commanders": self.get_watch_commanders()
        }
