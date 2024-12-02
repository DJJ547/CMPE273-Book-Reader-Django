from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse, FileResponse
import edge_tts
from edge_tts import Communicate
from django.core.cache import cache
import hashlib
import asyncio
import tempfile
import os
from django.conf import settings
from django.conf.urls.static import static
import json
import re

## other modules
from .mongodb import MongoDBFunctions
from bson import ObjectId
from .serializer import ChapterSerializer
# Create your views here.

@api_view(['GET'])
def getBook(request, book_name):
    mongo = MongoDBFunctions()
    chapters = mongo.getBook(book_name)
    if chapters and len(chapters) > 0:
        serializer = ChapterSerializer(list(chapters), many=True)
        return Response(serializer.data)
    else:
        return HttpResponse('Book not found', status=404)

@api_view(['GET'])
def getChapter(request, book_name, chapter_number):
    mongo = MongoDBFunctions()
    chapter = mongo.getChapter(book_name, chapter_number)
    if chapter:
        return Response(ChapterSerializer(chapter).data)
    else:
        return HttpResponse('Chapter not found', status=404)

@api_view(['GET'])
def getTableOfContents(request, book_name):
    mongo = MongoDBFunctions()
    chapters = mongo.getTableOfContents(book_name)
    if chapters:
        return Response(chapters)
    else:
        return HttpResponse('Book not found', status=404)
    
def sanitize_paragraph(paragraph):
    """
    Removes unsupported characters for Edge TTS.
    Only allows alphanumeric, common punctuation, and whitespace.
    """
    # Define the pattern for supported characters
    allowed_characters = re.compile(r"[^a-zA-Z0-9.,!?;:'\"()\[\]\s]")  # Add or adjust characters if necessary
    sanitized = allowed_characters.sub("", paragraph)  # Remove unsupported characters
    sanitized = re.sub(r"\s+", " ", sanitized).strip()  # Normalize whitespace
    return sanitized

async def generate_audio(paragraphs, voice, max_retries=2):
    timings = []
    audio_data = b""
    current_time = 0

    for paragraph in paragraphs:
        if paragraph.strip() == "":
            continue
        
        paragraph = sanitize_paragraph(paragraph)

        retries = 0
        while retries < max_retries:
            try:
                paragraph_audio = b""
                communicate = Communicate(text=paragraph, voice=voice)
                async for chunk in communicate.stream():
                    if "data" in chunk:
                        paragraph_audio += chunk["data"]

                # Calculate timing based on estimated WPM
                words = len(paragraph.split())
                average_wpm = 160  # Average words per minute
                paragraph_duration = (words / average_wpm) * 60 * 1000  # In milliseconds

                timings.append({
                    "start": current_time,
                    "end": current_time + paragraph_duration,
                    "text": paragraph,
                })
                current_time += paragraph_duration
                audio_data += paragraph_audio
                break  # Exit retry loop on success
            except edge_tts.exceptions.NoAudioReceived as e:
                print(f"Retrying due to: {e}")
                retries += 1
                await asyncio.sleep(2)  # Backoff delay
        else:
            print(f"Failed to process paragraph after {max_retries} retries.")

    return audio_data, timings



# Function to chunk paragraphs
def chunk_paragraphs(paragraphs, chunk_size=5):
    """
    Divides paragraphs into chunks of the given size.
    """
    for i in range(0, len(paragraphs), chunk_size):
        yield paragraphs[i:i + chunk_size]


# Function to stream audio
def stream_audio(audio_data):
    """
    Generator function to stream audio data in chunks.
    """
    chunk_size = 8192
    for i in range(0, len(audio_data), chunk_size):
        yield audio_data[i:i + chunk_size]


@api_view(['POST', 'GET'])
def tts_stream(request):
    """
    API endpoint to generate text-to-speech audio for a list of paragraphs.
    """
    # Get paragraphs and voice from the request
    paragraphs = request.data.get("paragraphs", [])
    voice = request.data.get("voice", "en-US-AriaNeural")

    if not paragraphs:
        return JsonResponse({"error": "No paragraphs provided"}, status=400)

    # Generate a unique cache key based on the input
    cache_key = hashlib.sha256(json.dumps({"paragraphs": paragraphs, "voice": voice}).encode()).hexdigest()

    # Check if the result is already in the cache
    cached_data = cache.get(cache_key)
    if cached_data:
        cached_audio_data = cached_data["audio_data"]
        cached_timings = cached_data["timings"]

        response = StreamingHttpResponse(stream_audio(cached_audio_data), content_type="audio/mpeg")
        response["Content-Disposition"] = 'inline; filename="audio.mp3"'
        response["X-Paragraph-Timings"] = json.dumps(cached_timings)
        response['Access-Control-Expose-Headers'] = 'X-Paragraph-Timings'
        return response

    # Generate audio and timings for the paragraphs
    combined_audio_data = b""
    combined_timings = []
    current_time = 0

    for chunk in chunk_paragraphs(paragraphs, chunk_size=1):
        audio_data, timings = asyncio.run(generate_audio(chunk, voice))
        combined_audio_data += audio_data

        # Adjust timings for the combined audio
        for timing in timings:
            timing["start"] += current_time
            timing["end"] += current_time
            combined_timings.append(timing)

        current_time = combined_timings[-1]["end"] if combined_timings else 0

    # Cache the generated audio and timings
    cache.set(cache_key, {"audio_data": combined_audio_data, "timings": combined_timings}, timeout=3600)

    # Serve the audio as a streaming response
    response = StreamingHttpResponse(stream_audio(combined_audio_data), content_type="audio/mpeg")
    response["Content-Disposition"] = 'inline; filename="audio.mp3"'
    response["X-Paragraph-Timings"] = json.dumps(combined_timings)
    response['Access-Control-Expose-Headers'] = 'X-Paragraph-Timings'

    return response




