

# Get the domain name from a URL
# Example: https://www.example.com/path?query=123 -> example
def get_domain_name(url):
    # Remove the protocol if present
    domain = url.split("://")[-1]
    # Remove any path or query parameters
    domain = domain.split("/")[0].split("?")[0]
    # Split the domain by "." and return the first part
    parts = domain.split(".")
    return parts[-2] if len(parts) >= 2 else parts[-1]


#
# # Global variables
# EXCEL_PATH = "results/oauth_test_results.xlsx"
# EVIL_DOMAIN = "someevildomain.com"
# PROXY_BURP_PORT = 8080
# PROXY_PORT = 1337
# proxy = {'http': f'http://127.0.0.1:{PROXY_BURP_PORT}', 'https': f'http://127.0.0.1:{PROXY_BURP_PORT}'}
#
# # Initialize a global counter for OAuth requests
# oauth_request_counter = 0
#
# IS_TESTING_RUNNING = False
# oauth_test_objects = []
#
#
# def run_tests(flow_request):
#     global IS_TESTING_RUNNING
#     IS_TESTING_RUNNING = True
#     oauth_object = oauth.OAuthTestResult(flow_request.url)
#     if oauth_object.client_id == '':
#         print(f"{Fore.RED}[!]{Fore.RESET}{Fore.LIGHTBLUE_EX} No {Fore.LIGHTYELLOW_EX}client_id{Fore.LIGHTBLUE_EX} found in the URL, skipping the test\n")
#         IS_TESTING_RUNNING = False
#         return
#     print_oauht_object_details(oauth_object)
#
#     # Run the fuzzing function with the EVIL_DOMAIN variable
#     oauth_object = start_evil_scenarios(flow_request, EVIL_DOMAIN, proxy, oauth_object, print_oauht_scenario_callback)
#
#     oauth_test_objects.append(oauth_object)
#     excel.add_test_result_to_excel(EXCEL_PATH, oauth_object)
#     IS_TESTING_RUNNING = False
#
#
#
# def print_result_wrapper(title, attribute, color, max_length):
#     attribute = attribute if attribute else "N/A"
#     color = color if attribute != "N/A" else colors.RED_STR
#     colors.print_result(title, attribute, color, max_length)
#
#
# def print_oauht_object_details(oauht_obj):
#     colors.print_title("OAuth Object Details")
#     attributes = {
#         "URL": oauht_obj.original_url,
#         "OAuth Type": oauht_obj.oauth_type,
#         "Scopes": oauht_obj.scope,
#         "Client ID": oauht_obj.client_id,
#         "State": oauht_obj.state,
#         "Redirect URI": oauht_obj.redirect_uri,
#         "Response Type": oauht_obj.response_type
#     }
#
#     max_length = max(len(title) for title in attributes.keys())
#     for title, attribute in attributes.items():
#         print_result_wrapper(title, attribute, colors.YELLOW_STR, max_length)
#
#
# def print_oauht_scenario_callback(scenario):
#     # Extract the description and the result of the bypass redirect test
#     description = scenario.description
#     is_succeed_bypass_redirect = scenario.is_succeed
#     # Determine the color of the result based on the result of the bypass redirect test
#     result_color = colors.YELLOW_STR if is_succeed_bypass_redirect else colors.RED_STR
#     # Print the scenario using colors.print_result()
#     max_length = MAX_SCENARIO_DESCRIPTION_LENGTH
#     colors.print_result(description, is_succeed_bypass_redirect, result_color, max_length)
#
#
# def start_evil_scenarios(flow_request, evil_domain, proxy, oauth_object, print_oauht_scenario_callback):
#     colors.print_title("Testing Redirect URI Scenarios")
#     main_tester.test_redirect2(flow_request, evil_domain, proxy, oauth_object, print_oauht_scenario_callback)
#     # colors.print_title("Testing State Scenarios")
#     # main_tester.test_state(url, cookies, evil_domain, proxy, oauth_object, print_oauht_scenario_callback)
#     return oauth_object
