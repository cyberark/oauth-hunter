from selenium import webdriver
#from seleniumwire import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
# https://pypi.org/project/webdriver-manager/
from webdriver_manager.firefox import GeckoDriverManager

PROXY_HOST = '127.0.0.1'
PROXY_PORT = 8080

def set_proxy(firefox_profile):
    firefox_profile.set_preference("network.proxy.type", 1)
    firefox_profile.set_preference("network.proxy.http", PROXY_HOST)
    firefox_profile.set_preference("network.proxy.http_port", PROXY_PORT)
    firefox_profile.set_preference("network.proxy.ssl", PROXY_HOST)
    firefox_profile.set_preference("network.proxy.ssl_port", PROXY_PORT)
    firefox_profile.set_preference("network.proxy.ftp", PROXY_HOST)
    firefox_profile.set_preference("network.proxy.ftp_port", PROXY_PORT)
    firefox_profile.set_preference("network.proxy.socks", PROXY_HOST)
    firefox_profile.set_preference("network.proxy.socks_port", PROXY_PORT)
    firefox_profile.set_preference("network.proxy.no_proxies_on", "")

def set_optimized_firefox_profile(firefox_profile):
    firefox_profile.set_preference("permissions.default.image", 2)  # Disable images
    firefox_profile.set_preference("dom.ipc.plugins.enabled.libflashplayer.so", "false")  # Disable Flash
    firefox_profile.set_preference("javascript.enabled", False)  # Disable JavaScript if not needed
def selenium_firefox_crawl(new_url):
    from seleniumwire import webdriver  # Import from seleniumwire
    firefox_profile_path = r'C:\Users\<user>\appdata\Roaming\mozilla\Firefox\Profiles\<user>'
    # Create a Firefox profile instance
    firefox_profile = webdriver.FirefoxProfile(firefox_profile_path)
    #set_proxy(firefox_profile)
    #set_optimized_firefox_profile(firefox_profile)

    options = webdriver.FirefoxOptions()
    options.profile = firefox_profile
    #options.headless = True  # Enable headless mode
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    # Go to the Google home page
    driver.get(new_url)

    is_succeed_bypass_redirect = False
    # Access requests via the `requests` attribute
    for request in driver.requests:
        if request.response:
            # write an if statement that catch with regex "code=")
            # do it on get requests
            if request.method == 'GET' and 'code=' in request.url:
                result = "success" if request.response.status_code in [200, 302] else "failed"
                if result == "success":
                    content = request.response.body.decode('utf-8', errors='ignore')
                    # id="error_box" -> when the user is not logged in with facebook
                    # "URL Blocked" -> when the user is logged in with facebook and it blocked
                    # Don't use `'aaa' or 'bbb' in response.text` because it will return 'aaa' (read more on how OR works to understand it).
                    if not any(keyword in content for keyword in
                               ['id="error_box"', 'URL Blocked', 'Insecure Login Blocked']):
                        is_succeed_bypass_redirect = True

                # print(request.url)
                # print(request.response.status_code)
                # print(request.response.headers['Content-Type'])
                #print(request.response.body)

    driver.quit()
    return is_succeed_bypass_redirect


#
# def selenium_crawl2(new_url):
#
#     firefox_profile_path = r'C:\Users\<user>\appdata\Roaming\mozilla\Firefox\Profiles\<user>'
#     # Create a Firefox profile instance
#     firefox_profile = webdriver.FirefoxProfile(firefox_profile_path)
#
#     set_proxy(firefox_profile)
#
#     options = webdriver.FirefoxOptions()
#     # options.set_preference('profile', firefox_profile_path)
#     options.profile = firefox_profile
#     #options.headless = True  # Enable headless mode
#
#     driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
#     print(new_url)
#     driver.get(new_url)
#
#     a = 2
#     driver.quit()


class FirefoxCrawler:
    def __init__(self):
        from seleniumwire import webdriver  # Import from seleniumwire
        self.driver = None
        self.init_driver()

    def init_driver(self):
        from selenium.webdriver.firefox.options import Options
        firefox_profile_path = r'C:\Users\<user>\appdata\Roaming\mozilla\Firefox\Profiles\<user>'
        options = Options()
        set_proxy(options)
        options.set_preference('profile', firefox_profile_path)

        #firefox_profile = webdriver.FirefoxProfile()

        self.driver = webdriver.Firefox(options=options)

    def init_driver2(self):
        firefox_profile_path = r'C:\Users\<user>\appdata\Roaming\mozilla\Firefox\Profiles\<user>'
        firefox_profile = webdriver.FirefoxProfile(firefox_profile_path)
        set_proxy(firefox_profile)
        #set_optimized_firefox_profile(firefox_profile)

        print("[+] Firefox profile is set up successfully")
        options = webdriver.FirefoxOptions()
        #options.profile = firefox_profile
        #options.headless = True  # Enable headless mode

        options.add_argument("--disable-extensions")  # Disables all extensions

        # Initialize the driver once and reuse it
        print("[+] Initializing Firefox driver")
        self.driver = webdriver.Firefox(service=FirefoxService(), options=options)
        print("[+] Firefox driver is ready")

    def crawl(self, new_url):
        self.driver.get(new_url)
        print("[+] Crawling the URL")
        is_succeed_bypass_redirect = False
        if hasattr(self.driver, "requests"):
            for request in self.driver.requests:
                if request.response:
                    if request.method == 'GET' and 'code=' in request.url:
                        result = "success" if request.response.status_code in [200, 302] else "failed"
                        if result == "success":
                            content = request.response.body.decode('utf-8', errors='ignore')
                            if not any(keyword in content for keyword in ['id="error_box"', 'URL Blocked', 'Insecure Login Blocked']):
                                is_succeed_bypass_redirect = True
        else:
            print("[!] The driver does not have the requests attribute")
        return is_succeed_bypass_redirect

    def close_driver(self):
        if self.driver:
            self.driver.quit()

