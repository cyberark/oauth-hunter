from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

class ChromeCrawler:
    def __init__(self):
        self.driver = None
        self.init_driver()

    def init_driver(self):
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
        chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
        chrome_options.add_argument("--disable-extensions")  # Disable extensions
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        chrome_options.add_argument("--ignore-certificate-errors")  # Ignore certificate errors

        # Set preferences to speed up performance
        prefs = {
            "profile.managed_default_content_settings.images": 2,  # Disable images
            "profile.default_content_setting_values.notifications": 2,  # Disable notifications
            "profile.managed_default_content_settings.cookies": 2,  # Disable cookies
        }
        chrome_options.add_experimental_option("prefs", prefs)

        # Set up proxy settings
        seleniumwire_options = {
            'proxy': {
                'http': 'http://localhost:8080',
                'https': 'https://localhost:8080',
                'no_proxy': 'localhost,127.0.0.1'  # Bypass proxy for local addresses
            }
        }

        # Initialize the Chrome driver with proxy settings
        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options,
            seleniumwire_options=seleniumwire_options
        )

    def crawl(self, new_url):
        self.driver.get(new_url)

        is_succeed_bypass_redirect = False
        for request in self.driver.requests:
            if request.response:
                if request.method == 'GET' and 'code=' in request.url:
                    result = "success" if request.response.status_code in [200, 302] else "failed"
                    if result == "success":
                        content = request.response.body.decode('utf-8', errors='ignore')
                        if not any(keyword in content for keyword in ['id="error_box"', 'URL Blocked', 'Insecure Login Blocked']):
                            is_succeed_bypass_redirect = True
        return is_succeed_bypass_redirect

    def close_driver(self):
        if self.driver:
            self.driver.quit()

# # Usage:
# crawler = ChromeCrawler()
# is_success = crawler.crawl("https://example.com")
# crawler.close_driver()
