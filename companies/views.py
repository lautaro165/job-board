from rest_framework import generics
from rest_framework.exceptions import PermissionDenied

from django.db.models import Count

from .serializers import PublicCompanySerializer
from .models import Company
from .services import update_company_service

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