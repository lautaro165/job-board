from rest_framework import generics
from rest_framework.exceptions import PermissionDenied

from django.db.models import Count
from django.shortcuts import get_object_or_404

from .serializers import PublicCompanySerializer
from .models import Company

from jobs.serializers import JobPostListSerializer
from jobs.models import JobPost

# Create your views here.

class CompanyListCreateView(generics.ListCreateAPIView):
    serializer_class = PublicCompanySerializer
    
    def get_queryset(self):
        return Company.objects.annotate(
            followers_count=Count("followers")
        )
        
class CompanyRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = PublicCompanySerializer
    
    lookup_field = "id"
    lookup_url_kwarg = "company_id"
    
    def perform_update(self, serializer):
        
        company = self.get_object()
        
        if company.created_by != self.request.user:
            raise PermissionDenied()
        
        return serializer.save()
    
class CompanyJobListView(generics.ListAPIView):
    serializer_class = JobPostListSerializer
    
    def get_queryset(self):
        company_id = self.kwargs.get("company_id")
        
        get_object_or_404(Company, id=company_id)
        
        return JobPost.objects.filter(
            company_id=company_id, 
            status=JobPost.ACTIVE
        )