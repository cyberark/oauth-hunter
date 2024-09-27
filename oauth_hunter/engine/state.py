import json
from urllib3.exceptions import InsecureRequestWarning
import urllib3
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
urllib3.disable_warnings(InsecureRequestWarning)
from engine.scenarios import REDIRECT_URI_SCENARIOS, Scenario, CONTROL_GROUP
import requests

def test_state(original_url, cookies, evil_domain, proxy, oauth_object, print_oauht_scenario_callback):
    parsed_url = urlparse(original_url)
    query_params = parse_qs(parsed_url.query)

    if 'state' not in query_params:
        # No state scenario
        description = "No state parameter"
        new_query_params = query_params.copy()
        new_query_params.pop('state', None)
        new_query_string = urlencode(new_query_params, doseq=True)
        new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, new_query_string, parsed_url.fragment))
        response = requests.get(new_url, proxies=proxy, verify=False, cookies=cookies)
        # TODO: Check how to verify if it succeed or not, not enough to check the status code
        is_succeed_bypass_redirect = response.status_code in [200, 302]

        scenario = Scenario(description, description, new_url, is_succeed_bypass_redirect)
        oauth_object.add_to_scenarios(scenario)
        print_oauht_scenario_callback(scenario)
    else:
        state = query_params['state'][0]
        scenarios = []

        # Test with a hardcoded state
        hardcoded_state = "hardcodedstate"
        new_query_params = query_params.copy()
        new_query_params['state'] = [hardcoded_state]
        new_query_string = urlencode(new_query_params, doseq=True)
        new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, new_query_string, parsed_url.fragment))
        scenarios.append((new_url, "Hardcoded state"))

        # Test with modified JSON state
        try:
            state_json = json.loads(state)
            if isinstance(state_json, list) and len(state_json) > 0:
                state_json[0] = 'modified_evil'
            elif isinstance(state_json, dict):
                first_key = next(iter(state_json))
                state_json[first_key] = 'modified_evil'
            modified_state = json.dumps(state_json)
            new_query_params = query_params.copy()
            new_query_params['state'] = [modified_state]
            new_query_string = urlencode(new_query_params, doseq=True)
            new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, new_query_string, parsed_url.fragment))
            scenarios.append((new_url, "Modified JSON state"))
        except (json.JSONDecodeError, TypeError):
            pass

        for new_url, description in scenarios:
            response = requests.get(new_url, proxies=proxy, verify=False, cookies=cookies)
            # TODO: Check how to verify if it succeed or not, not enough to check the status code
            is_succeed_bypass_redirect = response.status_code in [200, 302]
            scenario = Scenario(description, description, new_url, is_succeed_bypass_redirect)
            oauth_object.add_to_scenarios(scenario)
            print_oauht_scenario_callback(scenario)

    return oauth_object