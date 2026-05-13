from django.db import models

from .models import JobPost

class JobPostQuerySet(models.QuerySet):
    def visible(self):
        return self.exclude(status=JobPost.ARCHIVED)