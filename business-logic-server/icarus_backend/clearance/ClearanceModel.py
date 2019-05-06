from django.db import models
from django.utils import timezone


class Clearance(models.Model):
    clearance_id = models.TextField(primary_key=True)
    created_by = models.TextField()
    state = models.TextField()
    message = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def as_dict(self):
        return {
            "id": self.clearance_id,
            "created_by": self.created_by,
            "state": self.state,
            "message": self.message,
            "date": self.date.isoformat()
        }