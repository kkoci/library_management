import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    author = django_filters.CharFilter(lookup_expr='icontains')
    genre = django_filters.ChoiceFilter(choices=Book.GENRE_CHOICES)
    publication_year = django_filters.NumberFilter(field_name='publication_date', lookup_expr='year')
    available_only = django_filters.BooleanFilter(method='filter_available')
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'publication_year', 'available_only']
    
    def filter_available(self, queryset, name, value):
        if value:
            return queryset.filter(available_copies__gt=0)
        return queryset
