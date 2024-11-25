from django.urls import path
from . import views

urlpatterns = [
    path('book/<str:book_name>/', views.getBook, name='getBook'),
    path('book/<str:book_name>/chapter/<int:chapter_number>/', views.getChapter, name='getChapter'),
    path('book/<str:book_name>/table_of_contents/', views.getTableOfContents, name='getTableOfContents'),
    path('audio/tts_stream/', views.tts_stream, name='tts_stream'),
]