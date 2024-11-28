from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_google = models.BooleanField(null=False, default=False)

    class Meta:
        unique_together = ('email', 'is_google')


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    book_name = models.CharField(max_length=100, null=False)
    author = models.CharField(max_length=45, null=False)
    book_link = models.CharField(max_length=100, null=False)
    book_cover = models.CharField(max_length=100, null=False)
    book_description = models.CharField(max_length=500, null=False)
    num_of_chapters = models.IntegerField(null=False)

    class Meta:
        db_table = 'books'


class BookChapter(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    chapter_number = models.IntegerField(null=False)
    chapter_title = models.CharField(max_length=100, null=False)

    class Meta:
        unique_together = ('book', 'chapter_number')
        db_table = 'book_chapters'


class BookGenre(models.Model):
    GENRE_CHOICES = [
        ('thriller', 'Thriller'),
        ('post_apocalyptic', 'Post-apocalyptic'),
        ('fantasy', 'Fantasy'),
        ('comedy', 'Comedy'),
        ('sci_fi', 'Sci-Fi'),
        ('romance', 'Romance'),
        ('action', 'Action'),
        ('historical', 'Historical'),
        ('josei', 'Josei'),
        ('xuanhuan', 'Xuanhuan'),
        ('mystery', 'Mystery'),
        ('crime', 'Crime'),
        ('martial_arts', 'Martial Arts'),
        ('adventure', 'Adventure')
    ]
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, null=False)

    class Meta:
        unique_together = ('book', 'genre')
        db_table = 'book_genres'


class Shelf(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=45, null=False)
    icon = models.CharField(max_length=45, default='mood', null=False)
    background_color = models.CharField(
        max_length=45, default='white', null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        unique_together = ('user', 'name')
        db_table = 'shelves'


class ShelfBook(models.Model):
    id = models.AutoField(primary_key=True)
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('shelf', 'book')  # Ensures a unique relationship between shelf and book
        db_table = 'shelf_books'


class WishlistBook(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        unique_together = ('user', 'book')
        db_table = 'wishlist_books'


class BookReview(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    review = models.CharField(max_length=500, null=False)
    rating = models.FloatField(null=False)

    class Meta:
        db_table = 'book_reviews'


class BookProgress(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    current_chapter = models.IntegerField(default=0, null=False)
    last_read_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        unique_together = ('user', 'book')
        db_table = 'book_progress'
