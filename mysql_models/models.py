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
    book = models.ForeignKey(Book, on_delete=models.CASCADE, primary_key=True)
    chapter_number = models.IntegerField(null=False)
    chapter_title = models.CharField(max_length=100, null=True)

    class Meta:
        unique_together = ('book_id', 'chapter_number')
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

    # book_id as a foreign key
    book = models.ForeignKey(Book, on_delete=models.CASCADE, primary_key=True)

    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, null=False)

    class Meta:
        unique_together = ('book_id', 'genre')  # Ensure each combination is unique
        db_table = 'book_genres'

    def __str__(self):
        return self.get_genre_display()  # Returns the human-readable name of the genre


class ReadingLists(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    name = models.CharField(max_length=45, null=True)
    description = models.CharField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    flag_color = models.CharField(max_length=45, null=True)

    class Meta:
        db_table = 'reading_list'  # Replace with your actual table name

    def __str__(self):
        return self.name


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
