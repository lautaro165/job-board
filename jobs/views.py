from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from rest_framework import status

from .models import JobPost
from .serializers import JobPostSerializer

# Create your views here.

@api_view(["GET"])
def get_jobs_list(request):
    jobs = JobPost.objects.all().order_by("?")
    serializer = JobPostSerializer(jobs, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)