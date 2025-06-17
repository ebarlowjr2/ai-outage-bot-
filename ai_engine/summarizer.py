import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_outages(outages):
    services = ', '.join([o['service'] for o in outages])
    prompt = f"""
    Summarize the following outages for a live stream audience:
    Outages reported: {services}.
    Keep it short, simple, and conversational.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a live stream tech outage announcer."},
            {"role": "user", "content": prompt}
        ]
    )

    summary = response.choices[0].message.content
    return summary
