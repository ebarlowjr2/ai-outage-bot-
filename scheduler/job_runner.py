import schedule
import time
import logging
from main import main as run_outage_check

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def job():
    """Scheduled job to check for outages"""
    logging.info("Running scheduled outage check...")
    try:
        run_outage_check()
    except Exception as e:
        logging.error(f"Scheduled job failed: {e}")

schedule.every(10).minutes.do(job)

if __name__ == "__main__":
    logging.info("Starting AI Outage Bot Scheduler...")
    
    # Run once on startup
    job()
    
    while True:
        schedule.run_pending()
        time.sleep(1)
