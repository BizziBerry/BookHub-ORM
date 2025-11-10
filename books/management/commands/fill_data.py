# Создаем файл с содержимым
from django.core.management.base import BaseCommand
from books.models import Publisher, Book, Store, Review
from django.utils import timezone

class Command(BaseCommand):
    help = 'Fill database with test data'

    def handle(self, *args, **options):
        # Очищаем старые данные
        Review.objects.all().delete()
        Book.objects.all().delete()
        Publisher.objects.all().delete()
        Store.objects.all().delete()

        # Создаем издательства
        publishers = [
            Publisher(name="Эксмо", country="Россия"),
            Publisher(name="АСТ", country="Россия"), 
            Publisher(name="Penguin", country="Великобритания"),
            Publisher(name="Манн, Иванов и Фербер", country="Россия"),
        ]
        Publisher.objects.bulk_create(publishers)

        # Создаем книги
        books = [
            Book(
                title="Мастер и Маргарита",
                author="Михаил Булгаков", 
                published_date="1967-01-01",
                isbn="9785170903165",
                publisher=publishers[0]
            ),
            Book(
                title="Преступление и наказание",
                author="Федор Достоевский",
                published_date="1866-01-01", 
                isbn="9785170903172",
                publisher=publishers[0]
            ),
            Book(
                title="1984",
                author="Джордж Оруэлл",
                published_date="1949-06-08",
                isbn="9780141036144", 
                publisher=publishers[2]
            ),
            Book(
                title="Атомные привычки",
                author="Джеймс Клир", 
                published_date="2018-10-16",
                isbn="9785001464687",
                publisher=publishers[3]
            ),
        ]
        Book.objects.bulk_create(books)

        # Создаем магазины
        stores = [
            Store(name="Читай-город", city="Москва"),
            Store(name="Буквоед", city="Санкт-Петербург"),
            Store(name="Лабиринт", city="Москва"),
            Store(name="Московский Дом Книги", city="Москва"),
        ]
        Store.objects.bulk_create(stores)

        # Добавляем книги в магазины
        stores[0].books.add(books[0], books[1], books[2], books[3])
        stores[1].books.add(books[0], books[2])
        stores[2].books.add(books[1], books[3])
        stores[3].books.add(books[0], books[1], books[3])

        # Создаем отзывы
        reviews = [
            Review(book=books[0], rating=5, comment="Отличная книга!"),
            Review(book=books[0], rating=4, comment="Интересно, но сложно"),
            Review(book=books[1], rating=5, comment="Шедевр!"),
            Review(book=books[2], rating=4, comment="Актуально и сегодня"),
            Review(book=books[3], rating=5, comment="Полезная книга"),
        ]
        Review.objects.bulk_create(reviews)

        self.stdout.write(
            self.style.SUCCESS('База данных успешно заполнена тестовыми данными!')
        )