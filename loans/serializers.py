from rest_framework import serializers
from django.utils import timezone
from .models import Loan
from books.serializers import BookListSerializer
from users.serializers import UserSerializer

class LoanSerializer(serializers.ModelSerializer):
    book_details = BookListSerializer(source='book', read_only=True)
    user_details = UserSerializer(source='user', read_only=True)
    days_overdue = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    
    class Meta:
        model = Loan
        fields = ['id', 'user', 'book', 'loan_date', 'due_date', 'return_date', 
                 'status', 'fine_amount', 'notes', 'book_details', 'user_details',
                 'days_overdue', 'is_overdue']
        read_only_fields = ['loan_date', 'status', 'fine_amount']
    
    def validate(self, data):
        book = data.get('book')
        user = data.get('user')
        
        if book and not book.is_available:
            raise serializers.ValidationError("Book is not available for loan")
        
        # Check if user already has this book on loan
        if book and user and Loan.objects.filter(
            user=user, book=book, status='active'
        ).exists():
            raise serializers.ValidationError("User already has this book on loan")
        
        return data

class LoanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['book', 'notes']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
