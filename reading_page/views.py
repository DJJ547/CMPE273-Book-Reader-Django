from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from edge_tts import Communicate
import asyncio

## other modules
from .mongodb import MongoDBFunctions
from bson import ObjectId
from .serializer import ChapterSerializer
# Create your views here.

@api_view(['GET'])
def getBook(request, book_name):
    mongo = MongoDBFunctions()
    chapters = mongo.getBook(book_name)
    if len(chapters) > 0:
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
    
# Streaming TTS View
@api_view(['GET'])
def tts_stream(request):
    paragraph = request.GET.get("paragraph", None)
    voice = request.GET.get("voice", "en-US-AriaNeural")  # Default to a voice

    if not paragraph:
        return StreamingHttpResponse("No paragraph provided", status=400)

    async def generate_audio():
        try:
            communicate = Communicate(text=paragraph, voice=voice)
            async for chunk in communicate.stream():
                # Only yield if "data" is present in the chunk
                if "data" in chunk:
                    yield chunk["data"]
        except Exception as e:
            print(f"Error generating audio: {e}")
            yield b""

    # Wrapper to convert async generator to sync generator
    def audio_stream():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        generator = generate_audio()

        try:
            while True:
                chunk = loop.run_until_complete(generator.__anext__())
                yield chunk
        except StopAsyncIteration:
            pass
        finally:
            loop.close()

    # Create the HTTP response
    response = StreamingHttpResponse(audio_stream(), content_type="audio/mpeg")
    response["Content-Disposition"] = "inline; filename=tts_audio.mp3"
    return response




