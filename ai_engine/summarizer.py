import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def summarize_outages(outages):
    """Generate AI summary of outages using OpenAI GPT-4o"""
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logging.warning("OPENAI_API_KEY not found, using fallback summary")
            services = ', '.join([o['service'] for o in outages])
            return f"🚨 TECH OUTAGE ALERT: Current issues reported with {services}. Stay tuned for updates!"
        
        client = OpenAI(api_key=api_key)
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
        logging.info("AI summary generated successfully")
        return summary
        
    except Exception as e:
        logging.error(f"OpenAI summarization failed: {e}")
        services = ', '.join([o['service'] for o in outages])
        return f"🚨 TECH OUTAGE ALERT: Current issues reported with {services}. Stay tuned for updates!"
