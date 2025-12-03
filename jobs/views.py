from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import generics, status
from rest_framework.response import Response

from .models import JobPost
from .serializers import JobPostSerializer

# Create your views here.

class JobPostListCreateView(generics.ListCreateAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class JobPostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.owner != request.user:
            return Response({"error": "You cannot edit this job post"}, status=status.HTTP_403_FORBIDDEN)

        kwargs["partial"] = True

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.owner != request.user:
            return Response({"error": "You cannot delete this job post"}, status=403)

        return super().destroy(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()