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

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def edit_job_post(request, job_id):
    try:
        job_post = JobPost.objects.get(id=job_id)
    
    except JobPost.DoesNotExist:
        return Response({"error":f"There are no jobs with id {job_id}"},status=status.HTTP_404_NOT_FOUND)
    
    if job_post.owner != request.user:
        return Response({"error": "You cannot edit this job post"},status=status.HTTP_403_FORBIDDEN)
    
    data = request.data.copy()
    data["user"] = request.user.id
    updated_post = JobPostSerializer(data=data, instance=job_post, partial=True)
    
    if updated_post.is_valid():
        updated_post.save()
        return Response(updated_post.data, status=status.HTTP_200_OK)
    return Response(updated_post.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_job_post(request, job_id):
    try:
        job_post = JobPost.objects.get(id=job_id)
    except JobPost.DoesNotExist:
        return Response(
            {"error": f"There are no jobs with id {job_id}"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if job_post.owner != request.user:
        return Response(
            {"error": "You cannot delete this job post"},
            status=status.HTTP_403_FORBIDDEN
        )

    job_post.delete()
    return Response(
        {"message": f"Job post with id {job_id} has been deleted"},
        status=status.HTTP_204_NO_CONTENT
    )