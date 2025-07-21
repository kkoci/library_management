from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken
from books.models import Book
from loans.models import Loan
from datetime import date

User = get_user_model()

class BookViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            user_type='admin'
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
    
    def test_book_list_anonymous(self):
        response = self.client.get(reverse('book-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_book_list_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('book-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_book_create_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'isbn': '9876543210987',
            'genre': 'mystery',
            'publication_date': date.today(),
            'publisher': 'New Publisher',
            'page_count': 300,
            'total_copies': 3,
            'available_copies': 3,
        }
        response = self.client.post(reverse('book-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_book_create_regular_user(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'isbn': '9876543210987',
            'genre': 'mystery',
            'publication_date': date.today(),
            'publisher': 'New Publisher',
            'page_count': 300,
            'total_copies': 3,
            'available_copies': 3,
        }
        response = self.client.post(reverse('book-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_book_search(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('book-list-create') + '?search=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_book_filter_by_genre(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('book-list-create') + '?genre=fiction')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
