from django.contrib import admin
from .models import Book, Publisher, Store, Review

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    list_filter = ('country',)
    search_fields = ('name',)

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    list_filter = ('city',)
    filter_horizontal = ('books',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'rating', 'created_at', 'short_comment')
    list_filter = ('rating', 'created_at')
    search_fields = ('book__title', 'comment')
    readonly_fields = ('created_at',)  # Сделать поле только для чтения
    def short_comment(self, obj):
        """Сокращенный комментарий для списка"""
        return obj.comment[:50] + "..." if len(obj.comment) > 50 else obj.comment
    short_comment.short_description = "Комментарий"

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publisher', 'published_date')
    list_filter = ('author', 'publisher', 'published_date')
    search_fields = ('title', 'author', 'isbn')
    filter_horizontal = ('stores',)