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
        'Thriller', 'Post-apocalyptic', 'Fantasy', 'Comedy', 'Sci-Fi', 'Romance',  'Action', 'Historical', 'Josei', 'Xuanhuan', 'Mystery',  'Crime', 'Martial Arts', 'Adventure'
    ]

    # book_id as a foreign key
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre = models.CharField(
        max_length=20, choices=GENRE_CHOICES, null=False)
    
    class Meta:
        db_table = 'book_genres'
        

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
