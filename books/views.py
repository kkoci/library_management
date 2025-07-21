from django.shortcuts import render

from rest_framework import generics, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer, BookListSerializer
from .filters import BookFilter
from .permissions import IsAdminOrReadOnly

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'author', 'isbn', 'description']
    ordering_fields = ['title', 'author', 'publication_date', 'created_at']
    ordering = ['title']
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookListSerializer
        return BookSerializer

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def book_stats(request):
    total_books = Book.objects.count()
    available_books = Book.objects.filter(available_copies__gt=0).count()
    genres = Book.objects.values('genre').distinct().count()
    
    return Response({
        'total_books': total_books,
        'available_books': available_books,
        'genres': genres,
        'books_on_loan': total_books - available_books,
    })
