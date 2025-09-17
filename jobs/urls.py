from django.urls import path
from . import views

urlpatterns = [
    path("get-jobs-list/", views.get_jobs_list, name="get_jobs_list"),
    path("post-job/", views.post_job, name="post_job")
]