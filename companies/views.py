from rest_framework import generics

from django.db.models import Count

from .serializers import PublicCompanySerializer
from .models import Company

# Create your views here.

class CompanyListCreateView(generics.ListCreateAPIView):
    serializer_class = PublicCompanySerializer
    
    def get_queryset(self):
        return Company.objects.annotate(
            followers_count=Count("followers")
        )