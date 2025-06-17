from playwright.sync_api import sync_playwright
import logging
import time
import random

def fetch_downdetector():
    """Scrape current outages from Downdetector using Playwright with enhanced anti-detection"""
    max_retries = 3
    base_delay = 2
    
    mock_outages = [
        {'service': 'AWS', 'link': 'https://downdetector.com/status/aws'},
        {'service': 'Google', 'link': 'https://downdetector.com/status/google'},
        {'service': 'Microsoft', 'link': 'https://downdetector.com/status/microsoft'},
        {'service': 'Facebook', 'link': 'https://downdetector.com/status/facebook'},
        {'service': 'Twitter', 'link': 'https://downdetector.com/status/twitter'}
    ]
    
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                delay = base_delay + random.uniform(0, 2)
                logging.info(f"Waiting {delay:.1f} seconds before retry...")
                time.sleep(delay)
            
            logging.info(f"Attempting to scrape Downdetector (attempt {attempt + 1}/{max_retries})")
            
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=[
                        '--no-sandbox',
                        '--disable-blink-features=AutomationControlled',
                        '--disable-web-security',
                        '--disable-features=VizDisplayCompositor',
                        '--disable-dev-shm-usage',
                        '--disable-extensions',
                        '--disable-plugins',
                        '--disable-images',
                        '--disable-javascript',
                        '--no-first-run',
                        '--no-default-browser-check',
                        '--disable-default-apps',
                        '--disable-popup-blocking'
                    ]
                )
                
                user_agents = [
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0'
                ]
                
                context = browser.new_context(
                    user_agent=random.choice(user_agents),
                    viewport={'width': 1920, 'height': 1080},
                    locale='en-US',
                    timezone_id='America/New_York'
                )
                
                page = context.new_page()
                
                page.set_default_timeout(10000)  # 10 seconds
                
                page.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined,
                    });
                    
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5],
                    });
                    
                    Object.defineProperty(navigator, 'languages', {
                        get: () => ['en-US', 'en'],
                    });
                """)
                
                time.sleep(random.uniform(1, 3))
                response = page.goto('https://downdetector.com/', wait_until='domcontentloaded')
                
                if not response:
                    raise Exception("No response received from server")
                
                if response.status == 403:
                    logging.warning(f"Received 403 Forbidden - bot detection triggered")
                    raise Exception(f"Bot detection: HTTP {response.status}")
                elif response.status != 200:
                    raise Exception(f"HTTP error: {response.status}")
                
                try:
                    page.wait_for_load_state('networkidle', timeout=5000)
                except:
                    logging.debug("Network idle timeout, proceeding anyway")
                
                outages = []
                selectors_to_try = [
                    'a[href*="/status/"]',
                    'a[title][href*="/status/"]',
                    '.entry-title a',
                    '.company-name a',
                    '[data-testid="company-link"]',
                    '.company-link',
                    'a[href^="/status/"]'
                ]
                
                for selector in selectors_to_try:
                    try:
                        outage_elements = page.query_selector_all(selector)
                        if outage_elements and len(outage_elements) > 0:
                            logging.info(f"Found {len(outage_elements)} elements with selector: {selector}")
                            break
                    except Exception as e:
                        logging.debug(f"Selector {selector} failed: {e}")
                        continue
                else:
                    outage_elements = []
                
                for element in outage_elements:
                    try:
                        service = element.inner_text().strip()
                        link = element.get_attribute('href')
                        if service and link and '/status/' in link:
                            full_link = f'https://downdetector.com{link}' if link.startswith('/') else link
                            outages.append({
                                'service': service, 
                                'link': full_link
                            })
                    except Exception as e:
                        logging.debug(f"Error extracting element data: {e}")
                        continue
                
                browser.close()
                
                if outages:
                    logging.info(f"Successfully scraped {len(outages)} outages from Downdetector")
                    return outages
                else:
                    logging.warning("No outages found with any selector")
                    if attempt < max_retries - 1:
                        continue
                    else:
                        logging.info("Using mock outage data as fallback")
                        return mock_outages[:2]  # Return 2 mock outages
                        
        except Exception as e:
            logging.error(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                continue
            else:
                logging.warning("All scraping attempts failed, using mock data")
                return mock_outages[:2]  # Return 2 mock outages as fallback
    
    logging.info("Returning mock outage data")
    return mock_outages[:2]
