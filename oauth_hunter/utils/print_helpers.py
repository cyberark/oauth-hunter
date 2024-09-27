from utils import colors
from colorama import Fore
from engine.oauth_results import OAuthTestResult
from utils.excel import add_test_result_to_excel
from engine.scenarios import MAX_SCENARIO_DESCRIPTION_LENGTH, CONTROL_GROUP
from engine import redirect_uri
from . import config


IS_TESTING_RUNNING = False
oauth_test_objects = []
def print_result_wrapper(title, attribute, color, max_length):
    attribute = attribute if attribute else "N/A"
    color = color if attribute != "N/A" else colors.RED_STR
    colors.print_result(title, attribute, color, max_length)

def print_oauht_object_details(oauht_obj):
    #colors.print_title("OAuth Object Details")
    attributes = {
        "URL": oauht_obj.original_url,
        "OAuth Type": oauht_obj.oauth_type,
        "Scopes": oauht_obj.scope,
        "Client ID": oauht_obj.client_id,
        "State": oauht_obj.state,
        "Redirect URI": oauht_obj.redirect_uri,
        "Response Type": oauht_obj.response_type
    }

    max_length = max(len(title) for title in attributes.keys())
    for title, attribute in attributes.items():
        print_result_wrapper(title, attribute, colors.YELLOW_STR, max_length)

def print_oauht_scenario_callback(scenario):
    # Extract the description and the result of the bypass redirect test
    description = scenario.description
    is_succeed_bypass_redirect = scenario.is_succeed
    # Determine the color of the result based on the result of the bypass redirect test
    #result_color = colors.YELLOW_STR if is_succeed_bypass_redirect else colors.RED_STR

    # Determine the appropriate text and color based on the result of the bypass redirect test
    if is_succeed_bypass_redirect and (CONTROL_GROUP not in scenario.description):
        result_text = "Vulnerable"
        result_color = colors.RED_STR
    else:
        result_text = "Not Vulnerable"
        result_color = colors.YELLOW_STR

    # Print the scenario using colors.print_result()
    max_length = MAX_SCENARIO_DESCRIPTION_LENGTH

    colors.print_result(description, result_text, result_color, max_length, scenario.url)

def start_scenarios(flow_request, evil_domain, proxy, oauth_object, print_oauht_scenario_callback):
    colors.print_title("Testing Redirect URI Scenarios")
    #main_tester.test_redirect_uri2(flow_request, evil_domain, proxy, oauth_object, print_oauht_scenario_callback)
    oauth_object = redirect_uri.run(flow_request, evil_domain, proxy, oauth_object, print_oauht_scenario_callback)
    colors.print_end_title("Testing Redirect URI Scenarios")

    #main_tester.test_redirect_uri_any_path(flow_request, proxy, oauth_object, print_oauht_scenario_callback)
    #main_tester.test_redirect(flow_request, evil_domain, proxy, oauth_object, print_oauht_scenario_callback)
    # colors.print_title("Testing State Scenarios")
    # main_tester.test_state(url, cookies, evil_domain, proxy, oauth_object, print_oauht_scenario_callback)
    return oauth_object

def run_tests(flow_request):
    global IS_TESTING_RUNNING
    IS_TESTING_RUNNING = True

    oauth_object = OAuthTestResult(flow_request.url)
    if oauth_object.client_id == '':
        print(f"{Fore.RED}[!]{Fore.RESET}{Fore.LIGHTBLUE_EX} No {Fore.LIGHTYELLOW_EX}client_id{Fore.LIGHTBLUE_EX} found in the URL, skipping the test\n")
        IS_TESTING_RUNNING = False
        return
    print_oauht_object_details(oauth_object)

    # Run the fuzzing function with the EVIL_DOMAIN variable
    oauth_object = start_scenarios(flow_request, config.EVIL_DOMAIN, config.PROXY, oauth_object, print_oauht_scenario_callback)

    oauth_test_objects.append(oauth_object)
    global EXCEL_FULL_PATH
    add_test_result_to_excel(config.EXCEL_FULL_PATH, oauth_object)
    IS_TESTING_RUNNING = False
