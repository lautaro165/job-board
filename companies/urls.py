from django.urls import path
from .views import *

urlpatterns = [
    path("companies/", CompanyListCreateView.as_view()),
    path("companies/<int:company_id>/", CompanyRetrieveUpdateView.as_view()),
]