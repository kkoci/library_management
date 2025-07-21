from django.urls import path
from .views import BookListCreateView, BookDetailView, book_stats

urlpatterns = [
    path('', BookListCreateView.as_view(), name='book-list-create'),
    path('<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('stats/', book_stats, name='book-stats'),
]
