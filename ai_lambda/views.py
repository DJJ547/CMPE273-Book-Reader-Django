from rest_framework import status
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from .aws_sagemaker import invoke_sagemaker_chapter_summarization_endpoint, invoke_sagemaker_text_to_image_endpoint
import os
from django.core.files.base import ContentFile
import base64
from dotenv import load_dotenv
load_dotenv()


@api_view(['POST'])
def text_summarization_view(request):
    input_text = request.data.get('text', '')
    if not input_text:
        return Response({"error": "No text provided"}, status=status.HTTP_404_NOT_FOUND)
    
    summary = invoke_sagemaker_chapter_summarization_endpoint(input_text)
    return Response(summary, status=status.HTTP_200_OK)


@api_view(['POST'])
def image_generation_view(request):
    prompt = request.data.get('prompt', '')
    if not prompt:
        return Response({"error": "No prompt provided"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Prepend "give me a comic style of" to the user's input prompt
    full_prompt = f"{prompt}, in style of comic book art, cel shading, bold outlines, vibrant colors, dynamic comic panels and inked lines."
    
    try:
        image_base64 = invoke_sagemaker_text_to_image_endpoint(full_prompt)
        if not image_base64:
            return Response({"error": "No image generated"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Decode base64 image if you want to save it locally or return directly as response
        image_data = base64.b64decode(image_base64)
        image_file = ContentFile(image_data, name="generated_image.png")
        
        # Return as base64 encoded image string or link to saved image
        return Response({"generated_image": image_base64}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)