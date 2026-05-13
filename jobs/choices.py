from django.db import models

class JobStatuses(models.TextChoices):
    ACTIVE = 'active', 'Active'
    CLOSED = 'closed', 'Closed'
    PAUSED = 'paused', 'Paused'
    ARCHIVED = 'archived', 'Archived'