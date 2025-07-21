from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'genre', 'total_copies', 'available_copies', 'is_available']
    list_filter = ['genre', 'publication_date', 'language']
    search_fields = ['title', 'author', 'isbn']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'author', 'isbn', 'genre', 'publication_date', 'publisher')
        }),
        ('Details', {
            'fields': ('page_count', 'language', 'description', 'cover_image')
        }),
        ('Inventory', {
            'fields': ('total_copies', 'available_copies')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
