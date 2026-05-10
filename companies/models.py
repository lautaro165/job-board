from django.db import models
from users.models import CustomUser

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True, unique=True)
    logo = models.ImageField(upload_to="company_logos/", blank=True, null=True)
    
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="companies", null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    followers = models.ManyToManyField(CustomUser,related_name="followed_companies",blank=True)

    def __str__(self):
        return str(self.name)
