from django.test import TestCase
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from books.models import Book
from datetime import date

class BookModelTest(TestCase):
    def setUp(self):
        self.book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '1234567890123',
            'genre': 'fiction',
            'publication_date': date.today(),
            'publisher': 'Test Publisher',
            'page_count': 200,
            'total_copies': 5,
            'available_copies': 3,
        }
    
    def test_create_book(self):
        book = Book.objects.create(**self.book_data)
        self.assertEqual(book.title, 'Test Book')
        self.assertEqual(book.author, 'Test Author')
        self.assertTrue(book.is_available)
    
    def test_book_availability(self):
        book = Book.objects.create(**self.book_data)
        self.assertTrue(book.is_available)
        
        book.available_copies = 0
        book.save()
        self.assertFalse(book.is_available)
    
    def test_book_string_representation(self):
        book = Book.objects.create(**self.book_data)
        self.assertEqual(str(book), 'Test Book by Test Author')
    
    def test_available_copies_cannot_exceed_total(self):
        book_data = self.book_data.copy()
        book_data['available_copies'] = 10  # More than total_copies (5)
        book = Book.objects.create(**book_data)
        self.assertEqual(book.available_copies, book.total_copies)
