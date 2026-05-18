from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from django.shortcuts import get_object_or_404

from applications.serializers import ResumeAnalysisSerializer


from .serializers import JobPostCreateSerializer, JobPostSerializer, JobPostListSerializer
from .utils.pdf_handler import extract_text_from_pdf
from .utils.info import get_job_post_info
from .permissions import IsJobOwner
from .filters import JobPostFilter
from .choices import JobPostStatus
from .models import JobPost
from agent.agent_bridge import Agent

# Create your views here.

class JobPostListView(generics.ListAPIView):

    queryset = JobPost.objects.all()

    serializer_class = JobPostListSerializer

    permission_classes = [AllowAny]

    filterset_class = JobPostFilter

    ordering_fields = ["posted_at", "salary"]

    ordering = ["-posted_at"]
    
class JobPostCreateView(generics.CreateAPIView):

    queryset = JobPost.objects.all()

    serializer_class = JobPostCreateSerializer

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        serializer.save(
            posted_by=self.request.user
        )

class ResumeAnalysisView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ResumeAnalysisSerializer

    def post(self, request, *args, **kwargs):
        job_id = self.kwargs.get("job_id")
        
        job = get_object_or_404(JobPost, id=job_id)
        resume_file = request.FILES.get('resume')

        if not resume_file:
            return Response({"error": "No resume file provided"}, status=status.HTTP_400_BAD_REQUEST)

        resume_content = extract_text_from_pdf(resume_file)
        if not resume_content:
            return Response({"error": "Could not extract text from PDF"}, status=status.HTTP_400_BAD_REQUEST)

        job_post_info = get_job_post_info(job)

        ai_service = Agent()
        analysis = ai_service.analyze_resume_compatibility(
            resume_content=resume_content,
            job_post_info=job_post_info
        )

        if "error" in analysis:
            return Response(analysis, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response(analysis, status=status.HTTP_200_OK)

class GetOwnerJobPostListView(generics.ListAPIView):
    serializer_class = JobPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return JobPost.objects.filter(posted_by=self.request.user)

class JobPostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    permission_classes = [IsAuthenticated, IsJobOwner]

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)
    
    def perform_destroy(self, instance):
        instance.status = JobPostStatus.ARCHIVED
        instance.save()

class JobPostRetrieveView(generics.RetrieveAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    lookup_field = "id"
    lookup_url_kwarg = "job_id"

    def get_queryset(self):
        return JobPost.objects.filter(
            id=self.kwargs["job_id"]
        )