from rest_framework import status
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from .aws_sagemaker import invoke_sagemaker_chapter_summarization_endpoint, invoke_sagemaker_text_to_image_endpoint, summary_and_image
import os
from django.core.files.base import ContentFile
import base64
from dotenv import load_dotenv

load_dotenv()


# For Distilbart CNN 6-6
@api_view(['POST'])
def text_summarization_view(request):
    input_text = request.data.get('text', '')
    if not input_text:
        return Response({"error": "No text provided"}, status=status.HTTP_404_NOT_FOUND)
    
    summary = invoke_sagemaker_chapter_summarization_endpoint(input_text)
    return Response(summary, status=status.HTTP_200_OK)


# For Dreamlike Art Dreamlike Diffusion 1.0
@api_view(['POST'])
def image_generation_view(request):
    prompt = request.data.get('prompt', '')
    if not prompt:
        return Response({"error": "No prompt provided"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        result = summary_and_image(prompt)
        if not result:
            print("No image or summary generated")
            return Response({"error": "No image or summary generated"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        print("generated")
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)