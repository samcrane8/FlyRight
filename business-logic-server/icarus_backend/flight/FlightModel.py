from django.contrib.gis.db import models
from django.utils import timezone
from users.models import IcarusUser as User
from icarus_backend.clearance.ClearanceModel import Clearance
from icarus_backend.scheduling_rule.SchedulingRuleModel import SchedulingRule


class Flight(models.Model):
    id = models.TextField(primary_key=True)
    title = models.TextField()
    type = models.TextField()
    description = models.TextField()
    area = models.PolygonField(default='POLYGON EMPTY')
    created_at = models.DateTimeField(default=timezone.now)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    clearance = models.ForeignKey(Clearance,
                                  on_delete=models.SET_NULL,
                                  blank=True,
                                  null=True
                                  )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    scheduling_rule = models.ForeignKey(SchedulingRule,
                                        on_delete=models.SET_NULL,
                                        null=True)
    # clearance

    def as_geojson(self):
        return {
            "type": "FeatureCollection",
            "features": [
                {
                    "geometry": {
                        "coordinates": self.area[0].coords,
                        "type": "LineString"
                    }
                }
            ]
        }

    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "created_at": self.created_at.isoformat(),
            "area": self.as_geojson(),
            "starts_at": self.starts_at.isoformat(),
            "ends_at": self.ends_at.isoformat(),
            "created_by": self.created_by.id,
            "description": self.description,
            "commander_id": self.created_by.username,
            "clearance": self.clearance.as_dict(),
            "type": self.type,
            "scheduling": (self.scheduling_rule.as_dict() if self.scheduling_rule else {
                'frequency': 'Does Not Repeat', 'parameters': {'days': [],},
            }),
        }
