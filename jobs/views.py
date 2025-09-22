from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.core.paginator import Paginator

from .models import JobPost
from .serializers import JobPostSerializer

# Create your views here.

@api_view(["GET"])
def get_jobs_list(request):
    jobs = JobPost.objects.all().order_by("?")

    page_number = request.GET.get("page",1)
    paginator = Paginator(jobs, 10)
    page_jobs = paginator.get_page(page_number)
    
    return Response(JobPostSerializer(page_jobs, many=True).data,status=status.HTTP_200_OK)

@permission_classes([IsAuthenticated])
@api_view(["POST"])
def post_job(request):
    data = request.data

    serializer = JobPostSerializer(data=data, context={"user":request.user})

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)