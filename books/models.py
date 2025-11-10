from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Publisher(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название издательства")
    country = models.CharField(max_length=50, verbose_name="Страна")
    
    def __str__(self):
        return f"{self.name} ({self.country})"
    
    class Meta:
        verbose_name = "Издательство"
        verbose_name_plural = "Издательства"

class Store(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название магазина")
    city = models.CharField(max_length=50, verbose_name="Город")
    books = models.ManyToManyField('Book', related_name='stores', verbose_name="Книги")
    
    def __str__(self):
        return f"{self.name} ({self.city})"
    
    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"

class Review(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='reviews', verbose_name="Книга")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Оценка"
    )
    comment = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    def __str__(self):
        return f"Отзыв на {self.book.title} - {self.rating}/5"
    
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    author = models.CharField(max_length=100, verbose_name="Автор")
    published_date = models.DateField(verbose_name="Дата публикации")
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN")
    publisher = models.ForeignKey(
        Publisher, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='books',
        verbose_name="Издательство"
    )
    
    def __str__(self):
        return self.title
    
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0
    
    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"