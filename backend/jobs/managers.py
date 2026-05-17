from django.db import models
from .querysets import JobPostQuerySet

class JobPostManager(models.Manager.from_queryset(JobPostQuerySet)):
    def get_queryset(self):
        return super().get_queryset().visible()