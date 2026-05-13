from django.db import models

class JobStatuses(models.TextChoices):
    ACTIVE = 'active', 'Active'
    CLOSED = 'closed', 'Closed'
    PAUSED = 'paused', 'Paused'
    ARCHIVED = 'archived', 'Archived'
    
class EmploymentTypes(models.TextChoices):
    FULL_TIME = 'FT', 'Full-Time'
    PART_TIME = 'PT', 'Part-Time'
    REMOTE = 'RM', 'Remote'
    CONTRACT = 'CT', 'Contract'