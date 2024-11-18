from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=45, null=False)
    last_name = models.CharField(max_length=45, null=False)
    username = models.CharField(max_length=45, null=False, unique=True)
    password = models.CharField(max_length=45, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users'


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
    book = models.ForeignKey(Book, on_delete=models.CASCADE, primary_key=True)
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

    book = models.ForeignKey(Book, on_delete=models.CASCADE, primary_key=True)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, null=False)

    class Meta:
        unique_together = ('book', 'genre')
        db_table = 'book_genres'


# ==========================================================================================
class ReadingList(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    name = models.CharField(max_length=45, null=True)
    description = models.CharField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    flag_color = models.CharField(max_length=45, null=True)
    icon = models.CharField(max_length=45, null=True)
    is_favorite = models.BooleanField()

    class Meta:
        db_table = 'reading_lists'


class ReadingListBook(models.Model):
    UNREAD = 'unread'
    READING = 'reading'
    COMPLETED = 'completed'

    STATUS_CHOICES = [
        (UNREAD, 'unread'),
        (READING, 'reading'),
        (COMPLETED, 'completed'),
    ]

    reading_list_id = models.AutoField(primary_key=True)
    book_id = models.IntegerField()
    added_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=UNREAD)

    class Meta:
        unique_together = ('reading_list_id', 'book_id')
        db_table = 'reading_list_books'

    def __str__(self):
        return f"Book ID {self.book_id} - Status: {self.status}"
# ==========================================================================================


class Shelf(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=45, unique=True)
    icon = models.CharField(max_length=45, default='mood')
    background_color = models.CharField(max_length=45, default='white')
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        unique_together = ('user', 'name')
        db_table = 'shelves'


class ShelfBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, primary_key=True)
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        unique_together = ('shelf', 'book')
        db_table = 'shelf_books'
        

class WishlistBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        unique_together = ('user', 'book')
        db_table = 'wishlist_books'


class BookReview(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.CharField(max_length=500, null=False)
    rating = models.FloatField(null=False)

    class Meta:
        db_table = 'book_reviews'


class BookProgress(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_chapter = models.IntegerField(default=0, null=False)
    last_read_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        unique_together = ('user', 'book')
        db_table = 'book_progress'
