from colorama import Fore

PLUS = f"{Fore.YELLOW}[+]{Fore.RESET}"
BARRIER = f"{Fore.LIGHTGREEN_EX}===================================================={Fore.RESET}"

GREEN_STR = 'green'
RED_STR = 'red'
YELLOW_STR = 'yellow'
BLUE_STR = 'blue'
WHITE_STR = 'white'
def print_title(title):
    print(f"{BARRIER}( {Fore.LIGHTBLUE_EX}{title}{Fore.LIGHTBLUE_EX}{Fore.RESET} ){BARRIER}")

def print_end_title(title):
    line = "=" * len(title)
    print(f"{BARRIER}{Fore.LIGHTGREEN_EX}=={line}=={BARRIER}")
def print_result(subtitle, result, result_color, max_length, url=None):
    if result_color == GREEN_STR:
        result_color = Fore.LIGHTGREEN_EX
    elif result_color == RED_STR:
        result_color = Fore.LIGHTRED_EX
    elif result_color == YELLOW_STR:
        result_color = Fore.LIGHTYELLOW_EX
    else:
        result_color = Fore.WHITE

    #dots = '.' * (max_length - len(subtitle) + 3)  # Add 3 for the space and the dots
    dots = '.' * 6
    print(f"{PLUS}{Fore.LIGHTBLUE_EX} {subtitle.ljust(max_length)} {dots} {Fore.RESET}{result_color}{result}{Fore.RESET}")

    if url:
        print(f" └---- {Fore.LIGHTBLUE_EX} URL: {Fore.RESET}{Fore.LIGHTYELLOW_EX}{url}{Fore.RESET}")

def print_resultOLD(subtitle, result, result_color):
    if result_color == GREEN_STR:
        result_color = Fore.LIGHTGREEN_EX
    elif result_color == RED_STR:
        result_color = Fore.LIGHTRED_EX
    elif result_color == YELLOW_STR:
        result_color = Fore.LIGHTYELLOW_EX
    else:
        result_color = Fore.WHITE

    print(f"{PLUS}{Fore.LIGHTBLUE_EX} {subtitle} ... {Fore.RESET}{result_color}{result}{Fore.RESET}")