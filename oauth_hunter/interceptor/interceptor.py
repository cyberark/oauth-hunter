from mitmproxy import http
from colorama import Fore
import utils.colors as colors
import threading
from utils.print_helpers import run_tests
import re

oauth_request_counter = 0

# Do we want to catch "code=" ?
class OAuthInterceptor:
    def request(self, flow: http.HTTPFlow):
        if re.search(r"/(oauth|openid-connect).*(client_id=|redirect_uri=)", flow.request.url):
            if "oauth?encrypted_query" in flow.request.url:
                return
            global oauth_request_counter
            oauth_request_counter += 1
            # Construct the message with the incremented counter
            print('\n\n\n')
            title_message = f"OAuth request {Fore.YELLOW}#{oauth_request_counter}{Fore.LIGHTBLUE_EX} detected"
            colors.print_title(title_message)
            #colors.print_result('URL', flow.request.url, colors.WHITE_STR, 3)

            # import requests
            # session = requests.Session()
            # headers = {key: value for key, value in flow.request.headers.items()}
            # cookies = {key: value for key, value in flow.request.cookies.items()}
            # #session.cookies.update((cookies))
            # #session.headers.update(headers)
            # # Extract cookies from the flow
            # response = session.get(flow.request.url, proxies=proxy, verify=False, cookies=flow.request.cookies, headers=flow.request.headers, allow_redirects=False)
            # # Follow redirects and handle cookies
            # for history in response.history:
            #     session.cookies.update(history.cookies)
            #
            # # Handle redirects manually
            # while response.status_code == 302:
            #     # Follow redirects and handle cookies
            #     for history in response.history:
            #         session.cookies.update(history.cookies)
            #
            #     # Get the redirect location
            #     redirect_url = response.headers['Location']
            #
            #     # Perform the redirect manually
            #     response = session.get(redirect_url, proxies=proxy, verify=False, cookies=response.cookies, headers=response.headers,
            #                            allow_redirects=False)
            #
            # return

            thread1 = threading.Thread(target=run_tests, args=(flow.request,))
            # Start the threads
            thread1.start()
            # Wait for the threads to complete
            thread1.join()

            #flow.request.url = modify_request(flow.request.url)
            #print("[+] Modified URL: " + flow.request.url)


addons = [
    OAuthInterceptor()
]


