from django.db import models
from .choices import JobStatuses

class JobPostQuerySet(models.QuerySet):
    def visible(self):
        return self.exclude(status=JobStatuses.ARCHIVED)