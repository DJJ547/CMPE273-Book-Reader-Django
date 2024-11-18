import boto3
import json
from dotenv import load_dotenv
import os
load_dotenv()


def invoke_sagemaker_chapter_summarization_endpoint(input_text):
    client = boto3.client('sagemaker-runtime', region_name=os.getenv('AWS_DEFAULT_REGION_CHAP_SUM'))
    payload = {"inputs": input_text} 
    response = client.invoke_endpoint(
        EndpointName=os.getenv('AWS_SAGEMAKER_CHAP_SUM_ENDPOINT_NAME'),
        Body=json.dumps(payload),
        ContentType='application/x-text'
    )
    result = json.loads(response['Body'].read().decode('utf-8'))
    return result.get("summary_text", "No summary available.")


def invoke_sagemaker_text_to_image_endpoint(input_prompt):
    client = boto3.client('sagemaker-runtime', region_name=os.getenv('AWS_REGION'))
    payload = {"prompt": input_prompt}  # Adjust as per your model input specification
    
    response = client.invoke_endpoint(
        EndpointName=os.getenv('AWS_SAGEMAKER_TXT_TO_IMG_ENDPOINT_NAME'),
        Body=json.dumps(payload),
        ContentType='application/json'
    )
    
    # Assuming the model returns an image as a base64-encoded string
    result = json.loads(response['Body'].read().decode('utf-8'))
    image_base64 = result.get("generated_image", "")
    return image_base64