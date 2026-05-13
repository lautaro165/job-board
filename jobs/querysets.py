from django.db import models

class JobPostQuerySet(models.QuerySet):
    def visible(self):
        return self.exclude(status="ARCHIVED")
