from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from books.models import Book
from loans.models import Loan
from datetime import date

User = get_user_model()

class LoanViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            isbn='1234567890123',
            genre='fiction',
            publication_date=date.today(),
            publisher='Test Publisher',
            page_count=200,
            total_copies=5,
            available_copies=3,
        )
    
    def test_create_loan(self):
        self.client.force_authenticate(user=self.user)
        data = {'book': self.book.id}
        response = self.client.post(reverse('loan-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check that available copies decreased
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 2)
    
    def test_return_book(self):
        self.client.force_authenticate(user=self.user)
        loan = Loan.objects.create(user=self.user, book=self.book)
        self.book.available_copies = 2
        self.book.save()
        
        response = self.client.post(reverse('return-book', args=[loan.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that available copies increased
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 3)
        
        # Check loan status
        loan.refresh_from_db()
        self.assertEqual(loan.status, 'returned')
    
    def test_my_loans(self):
        self.client.force_authenticate(user=self.user)
        Loan.objects.create(user=self.user, book=self.book)
        
        response = self.client.get(reverse('my-loans'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
