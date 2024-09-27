# scenarios.py

#
# https://evil.com
# https://evil.www.legit.com - REMOVED
# https://evil.legit.com
# https://legit.com - CONTROL GROUP
# https://legit.com.evil.com
# https://www.legit.com@evil.com
# httsp://evil%ff@legit.com
# https://evil%ff.legit.com
# https://evil.com%ff@legit.com
# https://evil.com%bf:@legit.com
# https://evil.com／.legit.com
# https://evil.com\@legit.com
# https://legit.com\@evil.com
# 4evil.com://legit.com
# https://evil.com\[legit.com]
# https://legit.com.evil.com\@legit.com

CONTROL_GROUP = "Control Group"
# redirect_scenarios = [
#     #(f"https://{evil_domain}{original_path}", "Redirect to evil.com (preserve path)"),  # Change only domain, keep original path
#     #(f"https://evil.{legit_domain}{original_path}", "Subdomain of legit.com (evil.legit.com)"),  # Add evil as a subdomain, keep original path
#     #(f"https://{legit_domain}.evil.com{original_path}", "Legit domain inside evil domain (legit.com.evil.com)"),  # Legit domain inside evil.com, keep original path
#     (f"https://{legit_domain}@evil.com{original_path}", "Reverse @ symbol attack (legit.com@evil.com)"),  # Legit domain with evil.com after @, keep original path
#     #(f"https://evil.{legit_domain}{original_path}/%ff", "URL encoding of evil domain (evil.legit.com/%ff)"),  # Encoded attack, keep original path
#     #(f"https://{legit_domain}/any", "Replace path with /any"),  # Change path to "/any"
#     (original_redirect_uri, "Control group (no manipulation)")  # Control group for comparison
# ]


REDIRECT_URI_SCENARIOS = [
    (f"{{redirect_scheme}}{{legit_domain}}{{port}}{{original_path}}", f"Legitimate domain ({CONTROL_GROUP})"),
    (f"{{redirect_scheme}}{{evil_domain}}{{port}}{{original_path}}", "Redirect to evil.com (preserve path)"),  # Change only domain, keep original path
    (f"{{redirect_scheme}}{{evil_domain}}.{{legit_domain}}{{port}}{{original_path}}", "Subdomain 1 (evil.legit.com)"),  # Add evil as a subdomain, keep original path
    (f"{{redirect_scheme}}{{legit_domain}}.{{evil_domain}}{{port}}{{original_path}}", "Subdomain 2 (legit.com.evil.com)"),  # Legit domain inside evil.com, keep original path
    (f"{{redirect_scheme}}{{legit_domain}}{{port}}/any", "Replace path with /any"),  # Change path to "/any"
    (f"{{redirect_scheme}}{{legit_domain}}{{port}}{{original_path}}/any", "Replace path with /any at the end"),  # Change path to "/any" at the end

    (f"{{redirect_scheme}}{{evil_domain}}%0d%0a{{legit_domain}}{{port}}{{original_path}}", "Carrier trick (https://attacker.com%0d%0atarget.com)"),
    (f"//{{evil_domain}}{{port}}{{original_path}}", "No scheme (//attacker.com)"),
    # (f"{{redirect_scheme}}{{legit_domain}}@{{evil_domain}}{{port}}{{original_path}}", "Username trick (https://target.com@attacker.com)"),
    # (f"{{redirect_scheme}}{{evil_domain}}%ff@{{legit_domain}}{{port}}{{original_path}}", "Decode to question mark 1 (https://attacker%ff@target.com)"),
    # (f"{{redirect_scheme}}{{evil_domain}}%bf:@{{legit_domain}}{{port}}{{original_path}}", "Decode to question mark 2 (https://attacker.com%bf:@target.com)"),
    # (f"{{redirect_scheme}}{{evil_domain}}%ff@{{legit_domain}}{{port}}{{original_path}}", "Over-consumption 1 (https://attacker.com%ff@target.com)"),
    # (f"{{redirect_scheme}}{{evil_domain}}%ff.{{legit_domain}}{{port}}{{original_path}}", "Over-consumption 2 (https://attacker%ff.target.com)"),
    # (f"{{redirect_scheme}}{{evil_domain}}／.{{legit_domain}}{{port}}{{original_path}}", "Best fit mappings 1 (https://attacker.com/.target.com)"),
    # (f"{{redirect_scheme}}{{legit_domain}}／@{{evil_domain}}{{port}}{{original_path}}", "Best fit mappings 2 (https://target.com/@attacker.com)"),
    # (f"{{redirect_scheme}}{{evil_domain}}\\@{{legit_domain}}{{port}}{{original_path}}", "Evil Slash Trick 1 (https://attacker.com\@target.com)"),
    # (f"{{redirect_scheme}}{{legit_domain}}\\@{{evil_domain}}{{port}}{{original_path}}", "Evil Slash Trick 2 (https://target.com\@attacker.com)"),
    # (f"4{{evil_domain}}://{{legit_domain}}{{port}}{{original_path}}", "Scheme Manipulation"),
    # (f"{{redirect_scheme}}{{evil_domain}}\\[{{legit_domain}}]{{port}}{{original_path}}", "IPv6 Address Parsing Bug"),
    # (f"{{redirect_scheme}}{{legit_domain}}.{{evil_domain}}\\@{{legit_domain}}{{port}}{{original_path}}", "Combined Validator"),
]
# Calculate the maximum length of the scenario descriptions 'SCENARIOS'
MAX_SCENARIO_DESCRIPTION_LENGTH = max(len(description) for _, description in REDIRECT_URI_SCENARIOS)

BASE_HEADERS = [
    "Website", "Link", "OAuth Type", "scope", "response_type", "client_id", "oauth_link"
]

# Generate headers dynamically
HEADERS = BASE_HEADERS + [description for _, description in REDIRECT_URI_SCENARIOS]

REDIRECT_URI_TYPE = "redirect_uri"
STATE_TYPE = "state"
class Scenario:
    def __init__(self, name, type, description, url, is_succeed=False):
        self.name = name
        # The type of the scenario (e.g., "redirect_uri", "state")
        self.type = type
        self.description = description
        self.url = url
        self.is_succeed = is_succeed

    def __repr__(self):
        return (f"Scenario(name={self.name}, type={self.type}, description={self.description}, url={self.url}, is_succeed={self.is_succeed})")

def initialize_max_description_length(scenarios):
    global MAX_SCENARIO_DESCRIPTION_LENGTH
    MAX_SCENARIO_DESCRIPTION_LENGTH = max(len(scenario['description']) for scenario in scenarios)

def initialize_headers(scenarios):
    global HEADERS
    scenario_headers = [scenario['description'] for scenario in scenarios]
    HEADERS = BASE_HEADERS + scenario_headers

def initialize_redirect_uri_scenarios():
    scenarios = []
    for url, description in REDIRECT_URI_SCENARIOS:
        name = description
        type_ = REDIRECT_URI_TYPE
        scenario = Scenario(name=name, type=type_, description=description, url=url, is_succeed=False)
        scenarios.append(scenario)

#
# redirect_uri path traversal: https://hackerone.com/reports/1861974
# any path /~attacker

import yaml
# TODO: Add an option to load JSON with scenarios
def load_scenarios_from_yaml(yaml_path):
    with open(yaml_path, 'r', encoding='utf8') as file:
        data = yaml.safe_load(file)
    scenarios = [(item['url'], item['description']) for item in data['Scenarios']]
    return scenarios

