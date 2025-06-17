import os
import logging
from data_sources.downdetector_scraper import fetch_downdetector
from ai_engine.summarizer import summarize_outages
from streaming.tts_announcer import synthesize_speech
from streaming.obs_controller import switch_scene
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

def main():
    """Main application workflow"""
    logging.info("Starting AI Outage Bot...")
    
    os.makedirs("streaming/overlay", exist_ok=True)
    
    logging.info("Fetching Downdetector data...")
    outages = fetch_downdetector()
    
    if not outages:
        logging.info("No major outages found.")
        with open("streaming/overlay/output.txt", "w") as f:
            f.write("No major outages detected at this time.")
        return
    
    logging.info(f"Summarizing {len(outages)} outages...")
    summary = summarize_outages(outages)
    
    with open("streaming/overlay/output.txt", "w") as f:
        f.write(summary)
    logging.info("Summary written to overlay file")
    
    try:
        synthesize_speech(summary)
        logging.info("TTS audio generated")
    except Exception as e:
        logging.warning(f"TTS generation failed: {e}")
    
    try:
        switch_scene("Outage Live")
        logging.info("OBS scene switched")
    except Exception as e:
        logging.warning(f"OBS scene switching failed: {e}")
    
    print("\n====== Outage Summary ======")
    print(summary)

if __name__ == "__main__":
    main()
