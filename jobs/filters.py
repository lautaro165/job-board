import django_filters

from .models import JobPost

class JobPostFilter(django_filters.FilterSet):
    min_salary = django_filters.NumberFilter(field_name='salary', lookup_expr='gte')
    max_salary = django_filters.NumberFilter(field_name='salary', lookup_expr='lte')

    class Meta:
        model = JobPost
        fields = ["title", "owner", "company", "employment_type"]