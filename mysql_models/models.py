from django.db import models


class Book(models.Model):
    book_name = models.CharField(max_length=100, null=False)
    author = models.CharField(max_length=45, null=False)
    book_link = models.CharField(max_length=100, null=False)
    book_cover = models.CharField(max_length=100, null=False)
    book_description = models.CharField(max_length=500, null=False)

    def __str__(self):
        return self.book_name

    class Meta:
        db_table = 'books'


class BookChapter(models.Model):
    # book_id as a foreign key
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    chapter_number = models.IntegerField(null=False)
    chapter_title = models.CharField(max_length=100, null=True)

    class Meta:
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

     # Set book as a foreign key and primary key
    book = models.OneToOneField(Book, on_delete=models.CASCADE, primary_key=True)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, null=False)

    class Meta:
        unique_together = ('book_id', 'genre')  # Ensure each combination is unique
        db_table = 'book_genres' 

    def __str__(self):
        return self.get_genre_display()  # Returns the human-readable name of the genre


# class BookProgress(models.Model):
#     PROGRESS_CHOICES = [
#         ('unread', 'Unread'),
#         ('reading', 'Reading'),
#         ('completed', 'Completed'),
#     ]

#     user = models.ForeignKey(User, on_delete=models.CASCADE)  # user_id as a foreign key
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)  # book_id as a foreign key
#     current_chapter = models.IntegerField(default=0, null=False, blank=False)
#     progress = models.CharField(max_length=10, choices=PROGRESS_CHOICES, default='unread', null=False, blank=False)

#     class Meta:
#         unique_together = ('user', 'book')  # Ensures a unique progress entry per user-book pair

#     def __str__(self):
#         return f"{self.user.username} - {self.book.book_name} - {self.progress}"

class BookReview(models.Model):
    id = models.AutoField(primary_key=True)  # Primary key ID field
    book_id = models.IntegerField(null=False)  # ID of the book being reviewed
    user_id = models.IntegerField(null=False)  # ID of the user submitting the review
    review = models.TextField(null=False)  # Text of the review
    rating = models.IntegerField(null=False)  # Numerical rating, e.g., 1-5

    def __str__(self):
        return f"Review {self.id} for Book ID {self.book_id} by User ID {self.user_id}"

    class Meta:
        db_table = 'book_reviews'

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)  # Ensure the password is securely hashed
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the creation time

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

