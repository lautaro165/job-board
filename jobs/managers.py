from django.db import models
from .models import JobPost

class JobPostQuerySet(models.QuerySet):
    def active_jobs(self):
        return self.exclude(status=JobPost.ARCHIVED)

class JobPostManager(models.Manager):
    def get_queryset(self):
        return JobPostQuerySet(self.model, using=self._db).active_jobs()