from django.db import models

# First model (You may remove this if you don't need it)


class YourModelName(models.Model):
    field_name1 = models.CharField(max_length=100)
    field_name2 = models.IntegerField()
    # Add other fields as necessary

    def __str__(self):
        return self.field_name1  # or another string representation

# Book model


class Book(models.Model):
    book_name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    book_link = models.TextField()  # Use TextField for unlimited length
    book_cover = models.TextField()  # Use TextField for unlimited length
    book_description = models.TextField()  # Use TextField for unlimited length

    class Meta:
        db_table = 'books'  # Explicitly set the table name

    def __str__(self):
        return self.title
