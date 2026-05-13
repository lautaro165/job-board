from django.db import models
from .choices import JobPostStatus

class JobPostQuerySet(models.QuerySet):
    def visible(self):
        return self.exclude(status=JobPostStatus.ARCHIVED)
