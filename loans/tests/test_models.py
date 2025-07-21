from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta, date
from books.models import Book
from loans.models import Loan

User = get_user_model()

class LoanModelTest(TestCase):
    def setUp(self):
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
        loan = Loan.objects.create(
            user=self.user,
            book=self.book
        )
        self.assertEqual(loan.user, self.user)
        self.assertEqual(loan.book, self.book)
        self.assertEqual(loan.status, 'active')
        self.assertIsNotNone(loan.due_date)
    
    def test_loan_overdue_status(self):
        loan = Loan.objects.create(
            user=self.user,
            book=self.book,
            due_date=timezone.now() - timedelta(days=1)
        )
        loan.save()  # Trigger status update
        self.assertTrue(loan.is_overdue)
    
    def test_loan_return(self):
        loan = Loan.objects.create(
            user=self.user,
            book=self.book
        )
        loan.return_date = timezone.now()
        loan.save()
        self.assertEqual(loan.status, 'returned')
