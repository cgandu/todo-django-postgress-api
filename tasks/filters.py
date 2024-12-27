import django_filters
from .models import Task

class TaskFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Task
        fields = ['created_at']