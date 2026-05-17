from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import generics

from .filters import JobPostFilter
from .models import JobPost
from .permissions import IsJobOwner
from .serializers import JobPostCreateSerializer, JobPostSerializer, JobPostListSerializer
from .choices import JobPostStatus

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

# class JobPostListCreateView(generics.ListCreateAPIView):
#     queryset = JobPost.objects.all()
#     serializer_class = JobPostSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     filterset_class = JobPostFilter
#     ordering_fields = ["posted_at", "salary"]
#     ordering = ["-posted_at"]

#     def perform_create(self, serializer):
#         serializer.save(posted_by=self.request.user)

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