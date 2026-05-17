from django.db import models

class ApplicationStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    REVIEWED = "reviewed", "Reviewed"
    WITHDRAWN = "withdrawn", "Withdrawn"
    ACCEPTED = "accepted", "Accepted"
    REJECTED = "rejected", "Rejected"