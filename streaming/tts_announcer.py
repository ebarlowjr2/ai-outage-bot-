import boto3
import os

# Get AWS keys from env vars
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = "us-east-1"

polly_client = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION).client('polly')

def synthesize_speech(text, output_path="streaming/overlay/speech.mp3"):
    response = polly_client.synthesize_speech(
        VoiceId='Joanna',
        OutputFormat='mp3',
        Text=text
    )

    with open(output_path, 'wb') as file:
        file.write(response['AudioStream'].read())

    print(f"✅ Speech saved to {output_path}")
