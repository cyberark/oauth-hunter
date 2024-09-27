# oauth_results.py

from urllib.parse import urlparse, parse_qs
from utils.common_utils import get_domain_name

class OAuthTestResult:
    def __init__(self, url):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        self.original_url = url
        self.oauth_type = get_domain_name(parsed_url.netloc)
        self.response_type = query_params.get('response_type', [''])[0]
        self.client_id = query_params.get('client_id', [''])[0]
        self.scope = query_params.get('scope', [''])[0]
        self.state = query_params.get('state', [''])[0]
        self.redirect_uri = query_params.get('redirect_uri', [''])[0]
        self.domain = ''
        self._set_domain_name(query_params, self.redirect_uri)
        self.test_scenarios = []
        self.is_using_fb_sdk = self._is_using_fb_sdk(query_params)
        self.is_state_verified = False
        self.can_omit_state = False
        #self.is_redirect_uri_verified = False
        #self.is_redirect_uri_any_path_verified = False
        #self.is_redirect_uri_subdomain_verified = False

    def _is_using_fb_sdk(self, query_params):
        channel_url = query_params.get('channel_url', [''])[0]
        if channel_url is not None and channel_url.startswith('https://staticxx.facebook.com/'):
            return True
        return False
    def _set_domain_name(self, query_params, redirect_uri):
        self.domain = None
        if redirect_uri is not None:
            if redirect_uri.startswith('https://staticxx.facebook.com/'):
                self.domain = query_params.get('domain', [''])[0]
            else:
                self.domain = extract_legit_domain(redirect_uri)

    def add_to_scenarios(self, scenario):
        # Validate or process the scenario if needed
        self.test_scenarios.append(scenario)

    def __repr__(self):
        return (f"OAuthTestResult(response_type={self.response_type}, client_id={self.client_id}, "
                f"scope={self.scope}, state={self.state}, is_using_fb_sdk={self.is_using_fb_sdk}, is_state_verified={self.is_state_verified}, "
                f"can_omit_state={self.can_omit_state})")

def extract_legit_domain(redirect_uri):
    parsed_uri = urlparse(redirect_uri)
    domain = parsed_uri.netloc
    return domain