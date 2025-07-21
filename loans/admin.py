from django.contrib import admin
from .models import Loan

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'loan_date', 'due_date', 'return_date', 'status', 'fine_amount']
    list_filter = ['status', 'loan_date', 'due_date']
    search_fields = ['user__username', 'book__title', 'book__author']
    readonly_fields = ['loan_date', 'days_overdue', 'is_overdue']
    fieldsets = (
        ('Loan Information', {
            'fields': ('user', 'book', 'loan_date', 'due_date', 'return_date')
        }),
        ('Status', {
            'fields': ('status', 'fine_amount', 'days_overdue', 'is_overdue')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
    )
