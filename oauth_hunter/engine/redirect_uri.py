import requests
import urllib3
from urllib.parse import urlparse, urlunparse, urlencode, parse_qs
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
# Suppress only the single InsecureRequestWarning from urllib3 needed
urllib3.disable_warnings(InsecureRequestWarning)
from engine.scenarios import REDIRECT_URI_SCENARIOS, Scenario, CONTROL_GROUP


def check_response(response_text: str, content_type: str) -> bool:
    """
    Checks the response text to determine if a redirect bypass was successful.

    Args:
        response_text (str): The text content of the response.

    Returns:
        bool: True if bypassed, False otherwise.
    """
    # Normalize the response text to lowercase for easier comparison
    response_text_lower = response_text.lower()

    is_succeed_bypass_redirect = True
    # Define keywords and phrases indicating failure
    failure_indicators = [
        "invalid redirect",
        "invalid_request",
        "url blocked",  # Facebook
        "redirect uri",  # Facebook
        "redirect_uri"  # GitHub & Keycloak
    ]

    if 'text/html' in content_type:
        # Parse HTML to extract visible text
        soup = BeautifulSoup(response_text_lower, 'html.parser')
        #visible_text = soup.get_text(separator=' ').lower()
        # Extract the visible text only from meaningful tags (like body)
        visible_text = soup.body.get_text(separator=' ').lower() if soup.body else ''
    else:
        # For non-HTML responses, use the raw text
        visible_text = response_text_lower

    # Check for failure indicators
    for indicator in failure_indicators:
        if indicator in visible_text:
            is_succeed_bypass_redirect = False

    # If no failure indicators are found, assume bypass is successful
    return is_succeed_bypass_redirect


def run(flow_request, evil_domain, proxy, oauth_object, print_oauht_scenario_callback):
    """
    Tests various manipulations of redirect_uri to check for security issues in OAuth implementations.

    Args:
        flow_request: The original flow request with URL and cookies.
        evil_domain: The domain used for testing (e.g., attacker-controlled domain).
        proxy: The proxy settings used to route the requests.
        oauth_object: The OAuth object that stores test scenarios.
        print_oauht_scenario_callback: Callback function for logging and printing scenario results.

    Returns:
        The updated oauth_object with the results of the redirect_uri manipulations.
    """
    parsed_url = urlparse(flow_request.url)
    query_params = parse_qs(parsed_url.query)

    if 'redirect_uri' not in query_params:
        return oauth_object

    # Extract the original redirect_uri and parse it
    original_redirect_uri = query_params['redirect_uri'][0]
    parsed_redirect_uri = urlparse(original_redirect_uri)
    legit_domain = parsed_redirect_uri.netloc
    original_path = parsed_redirect_uri.path  # Keep the original path
    redirect_scheme = parsed_redirect_uri.scheme + "://"

    # Check if the netloc contains a port
    port = ''
    if ':' in parsed_redirect_uri.netloc:
        domain, port = parsed_redirect_uri.netloc.split(':')
        legit_domain = domain
        port = f":{port}"
        # If there is a port, prepend it to the path (for testing purposes)
        #if port:
        #    original_path = f"{port}{original_path}"

    # Define different scenarios for redirect_uri manipulations

    redirect_scenarios = [(scenario[0].format(redirect_scheme=redirect_scheme,
                                              evil_domain=evil_domain,
                                              legit_domain=legit_domain, port=port,
                                              original_path=original_path), scenario[1]) for scenario in REDIRECT_URI_SCENARIOS]

    # Iterate over each redirect scenario
    for fuzzed_redirect_uri, description in redirect_scenarios:
        # Replace the redirect_uri in the original URL query
        query_params['redirect_uri'] = [fuzzed_redirect_uri]

        new_query_string = urlencode(query_params, doseq=True)
        new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, new_query_string, parsed_url.fragment))

        # Send the request using the requests library
        try:
            response = requests.get(new_url, proxies=proxy, verify=False, cookies=flow_request.cookies, allow_redirects=True)
            # Determine success based on status code and response content
            result_succeed = True if response.status_code in [200, 302, 404] else False
            if result_succeed:
                content_type = response.headers.get('Content-Type', '')
                is_succeed_bypass_redirect = check_response(response.text, content_type)
            else:
                is_succeed_bypass_redirect = False

            # Create a scenario object to store the result
            scenario = Scenario(description, 'redirect_uri', description, new_url, is_succeed_bypass_redirect)
            oauth_object.add_to_scenarios(scenario)
            print_oauht_scenario_callback(scenario)

        except requests.exceptions.RequestException as e:
            from colorama import Fore
            print(f"{Fore.RED}[!]{Fore.RESET}{Fore.LIGHTBLUE_EX} Request failed for {description}: {e}")

    return oauth_object