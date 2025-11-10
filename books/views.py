from django.shortcuts import render
from django.db.models import Avg, Count
from .models import Book, Store

def optimized_queries_example(request):
    # Оптимизация с select_related() - для ForeignKey отношений
    books_with_publishers = Book.objects.select_related('publisher').all()
    
    # Оптимизация с prefetch_related() - для ManyToMany отношений
    stores_with_books = Store.objects.prefetch_related('books').all()
    
    # Комплексная оптимизация для книг с отзывами и магазинами
    books_with_all_relations = Book.objects.select_related('publisher').prefetch_related(
        'reviews', 'stores'
    ).all()

    # Сложные запросы из задания
    russian_books = Book.objects.filter(publisher__country='Россия')
    moscow_books = Book.objects.filter(stores__city='Москва').distinct()
    high_rated_books = Book.objects.annotate(
        avg_rating=Avg('reviews__rating')
    ).filter(avg_rating__gte=4.0)
    
    # 4. Подсчет количества книг, продающихся в каждом магазине
    stores_book_counts = Store.objects.annotate(books_count=Count('books'))
    
    # 5. Магазины, где продаются книги, опубликованные после 2010 года
    stores_with_recent_books = Store.objects.filter(
        books__published_date__year__gte=2010
    ).annotate(
        books_count=Count('books')
    ).order_by('-books_count')
    
    context = {
        'books_with_publishers': books_with_publishers,
        'stores_with_books': stores_with_books,
        'books_with_all_relations': books_with_all_relations,
        'russian_books': russian_books,
        'moscow_books': moscow_books,
        'high_rated_books': high_rated_books,
        'stores_book_counts': stores_book_counts,
        'stores_with_recent_books': stores_with_recent_books,
    }
    
    return render(request, 'index.html', context)