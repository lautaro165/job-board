from django.db import models

class JobPostQuerySet(models.QuerySet):
    def active_jobs(self):
        return self.exclude(status="ARCHIVED")

class JobPostManager(models.Manager):
    def get_queryset(self):
        return JobPostQuerySet(self.model, using=self._db).active_jobs()