from django.db import models
from users.models import CustomUser
from django.core.exceptions import ValidationError

from companies.models import Company

# Create your models here.

class JobPost(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    company = models.ForeignKey(Company,on_delete = models.CASCADE, related_name="jobs", null=True, blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    
    ACTIVE = 'AC'
    CLOSED = 'CL'
    PAUSED = 'PA'
    
    JOB_STATUSES = [
        (ACTIVE, 'Active'),
        (CLOSED, 'Closed'),
        (PAUSED, 'Paused'),
    ]
    
    status = models.CharField(
        max_length=2,
        choices=JOB_STATUSES,
        default=ACTIVE
    )
    
    FULL_TIME = 'FT'
    PART_TIME = 'PT'
    REMOTE = 'RM'
    CONTRACT = 'CT'
    
    EMPLOYMENT_TYPES = [
        (FULL_TIME, 'Full-Time'),
        (PART_TIME, 'Part-Time'),
        (REMOTE, 'Remote'),
        (CONTRACT, 'Contract'),
    ]
    
    employment_type = models.CharField(
        max_length=2,
        choices=EMPLOYMENT_TYPES,
        default=FULL_TIME
    )
    
    salary = models.PositiveIntegerField(null=True, blank=True)

    posted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    applicants = models.ManyToManyField(CustomUser, through="applications.Application", related_name="applied_jobs")

    def __str__(self):
        return f"{self.title} - {self.company or self.owner.username}"