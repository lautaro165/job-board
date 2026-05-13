import django_filters
from .models import Application

class ApplicationFilter(django_filters.FilterSet):
    applicant = django_filters.NumberFilter(field_name="applicant_id")

    job = django_filters.NumberFilter(field_name="job_id")

    created_after = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte"
    )

    created_before = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte"
    )
    
    class Meta:
        model = Application
        fields = [
            "status",
            "applicant",
            "job",
        ]