from django.urls import path
from . import views

urlpatterns = [
    path("get-jobs-list/", views.JobPostListCreateView.as_view(), name="get_jobs_list"),
    
    path("get-owner-jobs-list/", views.GetOwnerJobPostListView.as_view(), name="get_own_jobs_list"),
    
    path("post-job/", views.JobPostListCreateView.as_view(), name="post_job"),
    path("edit-job-post/<int:pk>/", views.JobPostRetrieveUpdateDestroyView.as_view(), name="edit_job_post"),
    path("delete-job-post/<int:pk>/", views.JobPostRetrieveUpdateDestroyView.as_view(), name="delete_job_post"),
    path("get-job-details/<int:job_id>/", views.JobPostRetrieveView.as_view(), name="get_job_details")
]