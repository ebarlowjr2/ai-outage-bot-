import schedule
import time
from data_sources.downdetector_scraper import fetch_downdetector
from ai_engine.summarizer import summarize_outages

def job():
    print("Running scheduled check...")
    outages = fetch_downdetector()

    if outages:
        summary = summarize_outages(outages)
        print("\n====== Outage Summary ======")
        print(summary)
        # Write summary to overlay file
        with open("streaming/overlay/output.txt", "w") as f:
            f.write(summary)
    else:
        print("No major outages found.")

# Every 10 minutes for now
schedule.every(10).minutes.do(job)

if __name__ == "__main__":
    print("Starting AI Outage Bot Scheduler...")
    job()  # Run once on startup
    while True:
        schedule.run_pending()
        time.sleep(1)
