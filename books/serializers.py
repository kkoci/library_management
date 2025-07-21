from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    is_available = serializers.ReadOnlyField()
    
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def validate_isbn(self, value):
        # Basic ISBN validation
        if not value.isdigit() or len(value) not in [10, 13]:
            raise serializers.ValidationError("ISBN must be 10 or 13 digits")
        return value
    
    def validate(self, data):
        if data.get('available_copies', 0) > data.get('total_copies', 0):
            raise serializers.ValidationError(
                "Available copies cannot exceed total copies"
            )
        return data

class BookListSerializer(serializers.ModelSerializer):
    is_available = serializers.ReadOnlyField()
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'genre', 'publication_date', 
                 'available_copies', 'total_copies', 'is_available', 'cover_image']
