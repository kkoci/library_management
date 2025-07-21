from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from books.models import Book

class Loan(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='loans')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='loans')
    loan_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-loan_date']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['book', 'status']),
            models.Index(fields=['due_date']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.status})"
    
    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = timezone.now() + timedelta(days=14)  # 2 weeks loan period
        
        # Update status based on dates
        if self.return_date:
            self.status = 'returned'
        elif timezone.now() > self.due_date and self.status == 'active':
            self.status = 'overdue'
        
        super().save(*args, **kwargs)
    
    @property
    def days_overdue(self):
        if self.status == 'overdue' and not self.return_date:
            return (timezone.now() - self.due_date).days
        return 0
    
    @property
    def is_overdue(self):
        return self.status == 'overdue' or (
            self.status == 'active' and timezone.now() > self.due_date
        )
