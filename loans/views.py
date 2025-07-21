from django.shortcuts import render

from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from .models import Loan
from .serializers import LoanSerializer, LoanCreateSerializer
from books.models import Book
from django.db import models

class LoanListView(generics.ListAPIView):
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return Loan.objects.all().select_related('user', 'book')
        return Loan.objects.filter(user=user).select_related('book')

class LoanCreateView(generics.CreateAPIView):
    serializer_class = LoanCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        with transaction.atomic():
            loan = serializer.save(user=self.request.user)
            # Decrease available copies
            book = loan.book
            book.available_copies -= 1
            book.save()

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def return_book(request, loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        
        # Check permissions
        if not request.user.is_admin and loan.user != request.user:
            return Response(
                {'error': 'You can only return your own books'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        if loan.status != 'active':
            return Response(
                {'error': 'Book is already returned'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with transaction.atomic():
            loan.return_date = timezone.now()
            loan.status = 'returned'
            
            # Calculate fine for overdue books
            if loan.is_overdue:
                days_overdue = loan.days_overdue
                loan.fine_amount = days_overdue * 0.50  # $0.50 per day
            
            loan.save()
            
            # Increase available copies
            book = loan.book
            book.available_copies += 1
            book.save()
        
        return Response(LoanSerializer(loan).data)
    
    except Loan.DoesNotExist:
        return Response(
            {'error': 'Loan not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_loans(request):
    loans = Loan.objects.filter(user=request.user).select_related('book')
    serializer = LoanSerializer(loans, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def loan_stats(request):
    if not request.user.is_admin:
        return Response(
            {'error': 'Admin access required'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    total_loans = Loan.objects.count()
    active_loans = Loan.objects.filter(status='active').count()
    overdue_loans = Loan.objects.filter(status='overdue').count()
    total_fines = Loan.objects.aggregate(
        total=models.Sum('fine_amount')
    )['total'] or 0
    
    return Response({
        'total_loans': total_loans,
        'active_loans': active_loans,
        'overdue_loans': overdue_loans,
        'total_fines': float(total_fines),
    })
