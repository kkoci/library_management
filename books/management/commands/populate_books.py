from django.core.management.base import BaseCommand
from books.models import Book
from datetime import date
import random

class Command(BaseCommand):
    help = 'Populate the database with sample books'
    
    def handle(self, *args, **options):
        sample_books = [
            {
                'title': 'To Kill a Mockingbird',
                'author': 'Harper Lee',
                'isbn': '9780061120084',
                'genre': 'fiction',
                'publication_date': date(1960, 7, 11),
                'publisher': 'J.B. Lippincott & Co.',
                'page_count': 376,
                'description': 'A gripping tale of racial injustice and childhood innocence.',
                'total_copies': random.randint(2, 10),
            },
            {
                'title': '1984',
                'author': 'George Orwell',
                'isbn': '9780451524935',
                'genre': 'sci_fi',
                'publication_date': date(1949, 6, 8),
                'publisher': 'Secker & Warburg',
                'page_count': 328,
                'description': 'A dystopian social science fiction novel.',
                'total_copies': random.randint(2, 10),
            },
            {
                'title': 'Pride and Prejudice',
                'author': 'Jane Austen',
                'isbn': '9780141439518',
                'genre': 'romance',
                'publication_date': date(1813, 1, 28),
                'publisher': 'T. Egerton',
                'page_count': 432,
                'description': 'A romantic novel of manners.',
                'total_copies': random.randint(2, 10),
            },
            {
                'title': 'The Great Gatsby',
                'author': 'F. Scott Fitzgerald',
                'isbn': '9780743273565',
                'genre': 'fiction',
                'publication_date': date(1925, 4, 10),
                'publisher': 'Charles Scribner\'s Sons',
                'page_count': 180,
                'description': 'A classic American novel set in the Jazz Age.',
                'total_copies': random.randint(2, 10),
            },
        ]
        
        for book_data in sample_books:
            book_data['available_copies'] = book_data['total_copies']
            book, created = Book.objects.get_or_create(
                isbn=book_data['isbn'],
                defaults=book_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created book: {book.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Book already exists: {book.title}')
                )
