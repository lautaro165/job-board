from django.db import models
from applications.choices import ApplicationStatus

class ApplicationQuerySet(models.QuerySet):
    def pending(self):
        return self.filter(status=ApplicationStatus.PENDING)
    
    def reviewed(self):
        return self.filter(status=ApplicationStatus.REVIEWED)
    
    def withdrawn(self):
        return self.filter(status=ApplicationStatus.WITHDRAWN)
    
    def accepted(self):
        return self.filter(status=ApplicationStatus.ACCEPTED)
    
    def rejected(self):
        return self.filter(status=ApplicationStatus.REJECTED)