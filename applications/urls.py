from django.urls import path
from . import views

urlpatterns = [
    path("apply-to-job/<int:job_id>/", views.apply_to_job, name="apply_to_job"),
    path("withdraw-application/<int:job_id>/", views.withdraw_application, name="withdraw_application"),
    path("get-user-applications/", views.get_user_applications, name="get_user_applications"),
]