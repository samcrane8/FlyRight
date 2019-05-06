import json

from django.contrib.gis.db import models


class SchedulingRule(models.Model):
    frequency = models.TextField()
    parameters = models.TextField()
    ends_at = models.DateTimeField()

    def as_dict(self):
        return {
            "frequency": self.frequency,
            "parameters": json.loads(self.parameters),
            "ends_at": self.ends_at.isoformat(),
        }
