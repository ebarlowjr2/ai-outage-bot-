from data_sources.downdetector_scraper import fetch_downdetector
from ai_engine.summarizer import summarize_outages

def main():
    print("Pulling Downdetector data...")
    
    # outages = fetch_downdetector()  # Disable real scraping for this test
    
    # Inject test data
    outages = [
        {'service': 'AWS'},
        {'service': 'Google Cloud'},
        {'service': 'Microsoft 365'},
        {'service': 'Xfinity'},
    ]

    if outages:
        summary = summarize_outages(outages)
        print("\n====== Outage Summary ======")
        print(summary)
    else:
        print("No major outages found.")

if __name__ == "__main__":
    main()
