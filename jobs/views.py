from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import generics, status
from rest_framework.response import Response

from .models import JobPost
from .permissions import IsJobOwner
from .serializers import JobPostSerializer

# Create your views here.

class JobPostListCreateView(generics.ListCreateAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class GetOwnerJobPostListView(generics.ListAPIView):
    serializer_class = JobPostSerializer
    permission_classes = [IsAuthenticated, IsJobOwner]

    def get_queryset(self):
        return JobPost.objects.filter(owner=self.request.user)

class JobPostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    permission_classes = [IsAuthenticated, IsJobOwner]

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)

class JobPostRetrieveView(generics.RetrieveAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    lookup_url_kwarg = "job_id"

    def get_queryset(self):
        return JobPost.objects.filter(
            id=self.kwargs["job_id"],
            owner=self.request.user
        )