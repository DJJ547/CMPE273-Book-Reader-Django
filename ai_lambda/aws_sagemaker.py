import boto3
import json
from dotenv import load_dotenv
import os
load_dotenv()


def invoke_sagemaker_chapter_summarization_endpoint(input_text):
    client = boto3.client(
    'sagemaker-runtime',
    region_name=os.getenv('AWS_DEFAULT_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)
    payload = {"inputs": input_text} 
    response = client.invoke_endpoint(
        EndpointName='jumpstart-dft-hf-summarization-dist-20241127-053131',
        Body=json.dumps(payload),
        ContentType='application/x-text'
    )
    result = json.loads(response['Body'].read().decode('utf-8'))
    return result.get("summary_text", "No summary available.")


def invoke_sagemaker_text_to_image_endpoint(input_prompt, resolution=(128, 128)):
    client = boto3.client(
    'sagemaker-runtime',
    region_name=os.getenv('AWS_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)
    payload = {"prompt": input_prompt, "width": resolution[0], "height": resolution[1]}
    response = client.invoke_endpoint(
        EndpointName='jumpstart-dft-drealike-art-diff-1-0-20241127-055724',
        Body=json.dumps(payload),
        ContentType='application/x-text',
        Accept='application/json'
    )
    # Assuming the model returns an image as a base64-encoded string
    result = json.loads(response['Body'].read().decode('utf-8'))
    image_base64 = result.get("generated_image", "")
    return image_base64