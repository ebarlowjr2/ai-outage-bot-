import boto3
import os
import logging
from dotenv import load_dotenv

load_dotenv()

def synthesize_speech(text, output_path="streaming/overlay/speech.mp3"):
    """Generate speech using Amazon Polly TTS"""
    try:
        # Get AWS keys from env vars
        aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        aws_region = os.getenv("AWS_REGION", "us-east-1")
        
        if not aws_access_key or not aws_secret_key:
            raise ValueError("AWS credentials not found in environment variables")
        
        polly_client = boto3.Session(
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=aws_region
        ).client('polly')
        
        response = polly_client.synthesize_speech(
            VoiceId='Joanna',
            OutputFormat='mp3',
            Text=text
        )

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'wb') as file:
            file.write(response['AudioStream'].read())

        logging.info(f"Speech saved to {output_path}")
        
    except Exception as e:
        logging.error(f"TTS synthesis failed: {e}")
        raise
