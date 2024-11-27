from django.urls import path
from .views import text_summarization_view, image_generation_view

urlpatterns = [
    path('summerize_chapter/', text_summarization_view, name='chapter summarization'),
    path('image_generation/', image_generation_view, name='generate image'),
]