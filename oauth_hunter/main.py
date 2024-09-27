import argparse
import random
import logging
from mitmproxy.tools.main import mitmdump
import sys
import os
import utils.common_utils
from utils.excel import handle_excel_file
from colorama import Fore
import utils.tips as tips  # Importing tips module
from engine.scenarios import initialize_headers, initialize_max_description_length, initialize_redirect_uri_scenarios, \
    load_scenarios_from_yaml
from oauth_hunter.utils import config

from utils import config

def print_logo():
    logo = fr'''{Fore.LIGHTGREEN_EX}
                    _   _           _                 _            
   ___   __ _ _   _| |_| |__       | |__  _   _ _ __ | |_ ___ _ __ 
  / _ \ / _` | | | | __| '_ \ _____| '_ \| | | | '_ \| __/ _ \ '__|
 | (_) | (_| | |_| | |_| | | |_____| | | | |_| | | | | ||  __/ |   
  \___/ \__,_|\__,_|\__|_| |_|     |_| |_|\__,_|_| |_|\__\___|_|   
                                                                   
    Author: Eviatar Gerzi (@g3rzi)
    Company: CyberArk
    Version: 1.0
    '''
    print(logo)


    # Logic:
    # 1. --create-excel <name>: Create an Excel file with the specified name.
    #    - If the name already exists, a unique filename is generated unless --overwrite is used.
    # 2. --create-excel (no name): Create an Excel file with the default name.
    #    - If the default file already exists, a unique filename is generated unless --overwrite is used.
    # 3. --create-excel <name> --overwrite: If the file exists, it will be overwritten, and the path will be set to the provided name.
    # 4. --create-excel --overwrite: If no name is provided, the default Excel filename is used, and if it exists, it will be overwritten.

def main():
    parser = argparse.ArgumentParser(description="OAuth Proxy Tester")
    parser.add_argument('--create-excel', nargs='?', const=config.EXCEL_DEFAULT_FILENAME,
                        help="Create an Excel file with the given name or use the default name.")
    parser.add_argument('--overwrite', action='store_true',
                        help="Overwrite the existing file if it exists.")
    parser.add_argument('--proxy-port', type=int, default=1337, help="Specify the proxy port.")
    #parser.add_argument('--burp-proxy', type=int, default=8080, help="Specify the Burp proxy port.")
    parser.add_argument('--burp-proxy', nargs='?', const=8080, type=int, default=None,
                        help="Specify the Burp proxy port. Defaults to 8080 if specified without a value.")
    parser.add_argument('--evil-domain', type=str, default="someevildomain.com", help="Specify the evil domain.")
    parser.add_argument('--yaml-scenarios', type=str, help="Path to YAML file with scenarios.")

    args = parser.parse_args()

    args.burp_proxy = 8080
    if args.burp_proxy:
        config.PROXY_PORT = args.proxy_port
        config.PROXY_BURP_PORT = args.burp_proxy
        proxy = {'http': f'http://127.0.0.1:{config.PROXY_BURP_PORT}', 'https': f'http://127.0.0.1:{config.PROXY_BURP_PORT}'}
        config.PROXY = proxy
        config.EVIL_DOMAIN = args.evil_domain

    print_logo()

    # if args.create_excel:
    #     # If the user specified a file name, generate a unique version of it
    #     unique_filename = utils.common_utils.get_unique_filename(args.create_excel)
    # else:
    #     # If no file name is specified, use the default name and make sure it's unique
    #     unique_filename = utils.common_utils.get_unique_filename(config.EXCEL_DEFAULT_FILENAME)
    #
    # # Set the final Excel path and create the Excel file
    # config.EXCEL_FULL_PATH = f"results/{unique_filename}"
    # create_excel_file(config.EXCEL_FULL_PATH)

    handle_excel_file(args.create_excel, args.overwrite)

    # Print a success message

    print(
        f"{Fore.YELLOW}[+]{Fore.RESET}{Fore.LIGHTBLUE_EX} Excel file created at '{Fore.LIGHTYELLOW_EX}{config.EXCEL_FULL_PATH}{Fore.LIGHTBLUE_EX}'{Fore.RESET}")

    #args.yaml_scenarios = "scenarios.yaml"
    if args.yaml_scenarios:
        loaded_scenarios = load_scenarios_from_yaml(args.yaml_scenarios)
        SCENARIOS = loaded_scenarios
        print(
            f"{Fore.YELLOW}[+]{Fore.RESET}{Fore.LIGHTBLUE_EX} Loaded scenarios from YAML file: {Fore.LIGHTYELLOW_EX}{args.yaml_scenarios}{Fore.LIGHTBLUE_EX}{Fore.RESET}")
        # Calculate the maximum length of the scenario descriptions
        initialize_max_description_length(SCENARIOS)
        # Generate headers dynamically
        initialize_headers(SCENARIOS)
    else:
        # Initialize scenarios
        initialize_redirect_uri_scenarios()

    logging.getLogger().setLevel(logging.CRITICAL)

    print(f"{Fore.YELLOW}[+]{Fore.RESET}{Fore.LIGHTBLUE_EX} Proxy started on port {Fore.LIGHTYELLOW_EX}{config.PROXY_PORT}{Fore.LIGHTBLUE_EX}{Fore.RESET}")
    if config.PROXY is not None:
        print(
            f"{Fore.YELLOW}[+]{Fore.RESET}{Fore.LIGHTBLUE_EX} Tests are using Burp Proxy started on port {Fore.LIGHTYELLOW_EX}{config.PROXY_BURP_PORT}{Fore.LIGHTBLUE_EX}{Fore.RESET}")

    # Print a random OAuth tip
    print(f"{Fore.YELLOW}[+]{Fore.RESET}{Fore.LIGHTYELLOW_EX} *{Fore.LIGHTBLUE_EX}Tip{Fore.LIGHTYELLOW_EX}*{Fore.LIGHTBLUE_EX}: {random.choice(tips.TIPS)}{Fore.RESET}")
    print(
        f"{Fore.YELLOW}[+]{Fore.RESET}{Fore.LIGHTBLUE_EX} Make sure you are logged in to the IdP you are testing{Fore.RESET}")

    interceptor_path = os.path.join(os.path.dirname(__file__), "interceptor", "interceptor.py")
    sys.argv = ["mitmdump", "-p", str(config.PROXY_PORT), "-q", "-s", interceptor_path]
    mitmdump()

if __name__ == "__main__":
    main()

# TODO:
# - The requirement file should contains:
# selenium-wire
# blinker<1.8.0
# The reason is because we will receive an error about 'blinker._saferef':
# https://github.com/seleniumbase/SeleniumBase/issues/2782
# It happens because from blinker versions 1.8 there is no more 'blinker_saferef' which the selenium-wire is using
# Because selenium-wire is not maintened anymore, we should install the latest version of blinker 1.7.0 which still support that.
