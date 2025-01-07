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
    # TODO: this one should be dynamic, replace one note in the part of the domain.
    (f"{{redirect_scheme}}é{{evil_domain}}{{port}}{{original_path}}", "IDN homograph with é"),

    # Domain bypasses
    (f"{{redirect_scheme}}{{evil_domain}}%0d%0a{{legit_domain}}{{port}}{{original_path}}", "Carrier trick (https://attacker.com%0d%0atarget.com)"),
    (f"//{{evil_domain}}{{port}}{{original_path}}", "No scheme (//attacker.com)"),
    (f"{{redirect_scheme}}{{legit_domain}}@{{evil_domain}}{{port}}{{original_path}}", "Username trick (https://target.com@attacker.com)"),
    (f"{{redirect_scheme}}{{evil_domain}}%ff@{{legit_domain}}{{port}}{{original_path}}", "Decode to question mark 1 (https://attacker%ff@target.com)"),
    (f"{{redirect_scheme}}{{evil_domain}}%bf:@{{legit_domain}}{{port}}{{original_path}}", "Decode to question mark 2 (https://attacker.com%bf:@target.com)"),
    (f"{{redirect_scheme}}{{evil_domain}}%ff@{{legit_domain}}{{port}}{{original_path}}", "Over-consumption 1 (https://attacker.com%ff@target.com)"),
    (f"{{redirect_scheme}}{{evil_domain}}%ff.{{legit_domain}}{{port}}{{original_path}}", "Over-consumption 2 (https://attacker%ff.target.com)"),
    (f"{{redirect_scheme}}{{evil_domain}}／.{{legit_domain}}{{port}}{{original_path}}", "Best fit mappings 1 (https://attacker.com/.target.com)"),
    (f"{{redirect_scheme}}{{legit_domain}}／@{{evil_domain}}{{port}}{{original_path}}", "Best fit mappings 2 (https://target.com/@attacker.com)"),
    (f"{{redirect_scheme}}{{evil_domain}}\\@{{legit_domain}}{{port}}{{original_path}}", "Evil Slash Trick 1 (https://attacker.com\@target.com)"),
    (f"{{redirect_scheme}}{{legit_domain}}\\@{{evil_domain}}{{port}}{{original_path}}", "Evil Slash Trick 2 (https://target.com\@attacker.com)"),
    (f"4{{evil_domain}}://{{legit_domain}}{{port}}{{original_path}}", "Scheme Manipulation"),
    (f"{{redirect_scheme}}{{evil_domain}}\\[{{legit_domain}}]{{port}}{{original_path}}", "IPv6 Address Parsing Bug"),
    (f"{{redirect_scheme}}{{legit_domain}}.{{evil_domain}}\\@{{legit_domain}}{{port}}{{original_path}}", "Combined Validator"),
    (f"{{evil_domain}}{{legit_domain}}{{port}}%2f%2f.{{legit_domain}}{{original_path}}", "Domain Bypass 1"),
    (f"{{evil_domain}}{{legit_domain}}{{port}}%5c%5c.{{legit_domain}}{{original_path}}", "Domain Bypass 2"),
    (f"{{evil_domain}}{{legit_domain}}{{port}}%3F.{{legit_domain}}{{original_path}}", "Domain Bypass 3"),
    (f"{{evil_domain}}{{legit_domain}}{{port}}%23.{{legit_domain}}{{original_path}}", "Domain Bypass 4"),
    # TODO: check about this 80 port, it can make problem if we have custom port, although it's not common.
    (f"{{redirect_scheme}}{{legit_domain}}{{port}}:80%40{{evil_domain}}{{original_path}}", "Domain Bypass 5"),
    (f"{{redirect_scheme}}{{legit_domain}}{{port}}%2e{{evil_domain}}{{original_path}}", "Domain Bypass 6"),

    # Path Confusion
    # Reference: https://dl.acm.org/doi/fullHtml/10.1145/3627106.3627140
    (f"{{redirect_scheme}}{{legit_domain}}{{port}}{{original_path}}/../../pwn", f"Basic Path traversal '/../../pwn'"),
    (f"{{redirect_scheme}}{{legit_domain}}{{port}}{{original_path}}/{{evil_domain}}", "Path Confusion 1"),
    (f"{{redirect_scheme}}{{legit_domain}}{{port}}{{original_path}}%2F{{evil_domain}}", "Path Confusion 2"),
    (f"{{redirect_scheme}}{{legit_domain}}{{port}}{{original_path}}/..%2F{{evil_domain}}", "Path Confusion 3"),
    (f"{{redirect_scheme}}{{legit_domain}}{{port}}{{original_path}}/%2e%2e%2F{{evil_domain}}", "Path Confusion 4"),
    (f"{{redirect_scheme}}{{legit_domain}}{{port}}{{original_path}}/..%252F{{evil_domain}}", "Path Confusion 5"),
    (f"{{redirect_scheme}}{{legit_domain}}{{port}}{{original_path}}/%252e%252e%252F{{evil_domain}}", "Path Confusion 6"),
    (f"{{redirect_scheme}}{{legit_domain}}{{port}}{{original_path}}/{{evil_domain}}/..", "Path Confusion 7"),
    (f"{{redirect_scheme}}{{legit_domain}}{{port}}{{original_path}}%2F{{evil_domain}}%2F..", "Path Confusion 8"),
    (f"{{redirect_scheme}}{{legit_domain}}{{port}}{{original_path}}%2F{{evil_domain}}%2F%2e%2e", "Path Confusion 9"),
    (f"{{redirect_scheme}}{{legit_domain}}{{port}}{{original_path}}%252F{{evil_domain}}%252F..", "Path Confusion 10"),
    (f"{{redirect_scheme}}{{legit_domain}}{{port}}{{original_path}}%252F{{evil_domain}}%252F%252e%252e", "Path Confusion 11"),
    (f"{{redirect_scheme}}{{legit_domain}}{{port}}{{original_path}}/;/../../{{evil_domain}}", "Path Confusion 12"),
    (f"{{redirect_scheme}}{{legit_domain}}{{port}}{{original_path}}/%3B/../../{{evil_domain}}", "Path Confusion 13"),
    (f"{{redirect_scheme}}{{legit_domain}}{{port}}{{original_path}}/%3B%2F..%2F..%2F{{evil_domain}}", "Path Confusion 14"),
    (f"{{redirect_scheme}}{{legit_domain}}{{port}}{{original_path}}/%3B%2F%2e%2e%2F%2F%2e%2e{{evil_domain}}", "Path Confusion 15"),
    (f"{{redirect_scheme}}{{legit_domain}}{{port}}{{original_path}}/%253B%252F..%252F..%252F{{evil_domain}}", "Path Confusion 16"),
    (f"{{redirect_scheme}}{{legit_domain}}{{port}}{{original_path}}/%0A%0D/../../{{evil_domain}}", "Path Confusion 17"),
    (f"{{redirect_scheme}}{{legit_domain}}{{port}}{{original_path}}/%0A%0D%2F..%2F..%2F{{evil_domain}}", "Path Confusion 18"),
    (f"{{redirect_scheme}}{{legit_domain}}{{port}}{{original_path}}/%0A%0D%2F%2e%2e%2F%2F%2e%2e{{evil_domain}}", "Path Confusion 19"),
    (f"{{redirect_scheme}}{{legit_domain}}{{port}}{{original_path}}/%250A%250D%252F..%252F..%252F{{evil_domain}}", "Path Confusion 20"),
    # Reference: https://github.com/snyff/oauthsecurity
    (f"{{redirect_scheme}}{{legit_domain}}{{port}}{{original_path}}/../../new/path", "Path Confusion 21"),
    (f"{{redirect_scheme}}{{legit_domain}}{{port}}{{original_path}}/%2e%2e/%2e%2e/new/path", "Path Confusion 22"),
    (f"{{redirect_scheme}}{{legit_domain}}{{port}}{{original_path}}/%252e%252e/%252e%252e/new/path", "Path Confusion 23"),
    (f"{{redirect_scheme}}{{legit_domain}}{{port}}/new/path///../../{{original_path}}", "Path Confusion 24"),
    (f"{{redirect_scheme}}{{legit_domain}}{{port}}{{original_path}}/.%0a./.%0d./new/path", "Path Confusion 25 (For Rails, because it strips \n\d\0)"),

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

