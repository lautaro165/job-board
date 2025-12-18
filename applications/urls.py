from django.urls import path
from . import views

urlpatterns = [
    path("apply-to-job/<int:job_id>/", views.ApplyToJobView.as_view(), name="apply_to_job"),
    path("responde-to-application/<int:application_id>/", views.RespondToApplicationView.as_view(), name="responde_to_application"),
    path("withdraw-application/<int:job_id>/", views.WithdrawApplicationView.as_view(), name="withdraw_application"),
    path("get-user-applications/", views.get_user_applications, name="get_user_applications"),
    path("get-job-applications/<int:job_id>/", views.get_job_applications, name="get_job_applications")
]