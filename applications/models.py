from django.db import models
from users.models import CustomUser
from jobs.models import JobPost

# Create your models here.

class Application(models.Model):
    applicant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)