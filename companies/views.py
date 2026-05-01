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
        
class CompanyRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = PublicCompanySerializer
    
    lookup_field = "id"
    lookup_url_kwarg = "company_id"
    
    #REESCRIBIR PARA VALIDAR QUE EL DUEÑO SEA EL QUE MODIFICA LA INFO
    def perform_update(self, serializer):
        return super().perform_update(serializer)