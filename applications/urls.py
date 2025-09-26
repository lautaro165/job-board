from django.urls import path
from . import views

urlpatterns = [
    path("apply-to-job/<int:job_id>/", views.apply_to_job, name="apply_to_job")
]