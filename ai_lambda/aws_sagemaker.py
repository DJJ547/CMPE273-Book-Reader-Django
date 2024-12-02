import boto3
import json
from dotenv import load_dotenv
import os
import hashlib
from django.core.cache import cache
import numpy as np
import base64
from PIL import Image
import io

load_dotenv()

def numpy_array_to_base64(image_array):
    """Convert a NumPy array to a base64-encoded string."""
    image = Image.fromarray(image_array)
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def base64_to_numpy_array(base64_str):
    """Convert a base64-encoded string to a NumPy array."""
    image_data = base64.b64decode(base64_str)
    image = Image.open(io.BytesIO(image_data))
    return np.array(image)

def invoke_sagemaker_chapter_summarization_endpoint(input_text):
    client = boto3.client('sagemaker-runtime', region_name=os.getenv('AWS_DEFAULT_REGION'), aws_access_key_id=os.getenv(
        'AWS_ACCESS_KEY_ID_CHAP_SUM'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY_CHAP_SUM'))
    if not client:
        print("Client not created.")
        return None
    payload = {"inputs": input_text}
    try:
        response = client.invoke_endpoint(
            EndpointName=os.getenv('AWS_SAGEMAKER_CHAP_SUM_ENDPOINT_NAME'),
            Body=json.dumps(payload),
            ContentType='application/x-text'
        )
        result = json.loads(response['Body'].read().decode('utf-8'))
        return result.get("summary_text", "No summary available.")
    except client.exceptions.ValidationError as e:
        return None
    except Exception as e:
        return None

def invoke_sagemaker_text_to_image_endpoint(input_prompt):
    cache_key = hashlib.sha256(json.dumps(
        {"input_prompt": input_prompt}).encode()).hexdigest()
    cached_data = cache.get(cache_key)
    if cached_data:
        print("Returning cached data.")
        return cached_data['image_base64']

    client = boto3.client('sagemaker-runtime', region_name=os.getenv('AWS_DEFAULT_REGION'), aws_access_key_id=os.getenv(
        'AWS_ACCESS_KEY_ID_CHAP_SUM'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY_CHAP_SUM'))
    if not client:
        print("Client not created.")
        return None
    print("Client created.")

    payload = {"prompt": input_prompt}
    try:
        response = client.invoke_endpoint(
            EndpointName=os.getenv('AWS_SAGEMAKER_TXT_TO_IMG_ENDPOINT_NAME'),
            Body=json.dumps(payload),
            ContentType='application/x-text',
            Accept='application/json'
        )
        print("Response received.")
        # Assuming the model returns an image array
        result = json.loads(response['Body'].read().decode('utf-8'))
        image_array = np.array(result.get("generated_image", []))
        
        # Convert the image array to a base64-encoded string
        image_base64 = numpy_array_to_base64(image_array)
        
        # Store the result in the cache with a timeout of 1 hour
        cache.set(cache_key, {"image_base64": image_base64}, timeout=3600)
        
        return image_base64
    except client.exceptions.ValidationError as e:
        return None
    except Exception as e:
        return None

def summary_and_image(input_prompt):
    summarys = []
    images_base64 = []
    print(len(input_prompt))    
    for i in range(len(input_prompt)):
        summary = invoke_sagemaker_chapter_summarization_endpoint(input_prompt[i])
        image_base64 = invoke_sagemaker_text_to_image_endpoint(input_prompt[i])
        if not summary or not image_base64:
            continue
        summarys.append(summary)
        images_base64.append(image_base64)
    return {"summaries": summarys, "images": images_base64}
