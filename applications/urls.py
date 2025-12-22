from django.urls import path
from . import views

urlpatterns = [
    path("apply-to-job/<int:job_id>/", views.ApplyToJobView.as_view(), name="apply_to_job"),
    path("respond-to-application/<int:application_id>/", views.RespondToApplicationView.as_view(), name="respond_to_application"),
    path("withdraw-application/<int:application_id>/", views.WithdrawApplicationView.as_view(), name="withdraw_application"),
    path("get-user-applications/", views.UserApplicationsListView.as_view(), name="get_user_applications"),
    path("get-job-applications/<int:job_id>/", views.JobApplicationsListView.as_view(), name="get_job_applications")
]