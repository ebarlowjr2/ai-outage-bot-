from playwright.sync_api import sync_playwright
import logging

def fetch_downdetector():
    """Scrape current outages from Downdetector using Playwright"""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto('https://downdetector.com/')
            
            page.wait_for_load_state('networkidle')
            
            outages = []
            outage_elements = page.query_selector_all('.entry-title a')
            
            for element in outage_elements:
                service = element.inner_text().strip()
                link = element.get_attribute('href')
                if service and link:
                    outages.append({
                        'service': service, 
                        'link': f'https://downdetector.com{link}' if link.startswith('/') else link
                    })
            
            browser.close()
            logging.info(f"Found {len(outages)} outages")
            return outages
            
    except Exception as e:
        logging.error(f"Error scraping Downdetector: {e}")
        return []
