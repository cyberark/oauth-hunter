from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

# TODO: Add login to facebook or GitHub

def start_crawl(target_url):
    proxy = "127.0.0.1:1337"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f'--proxy-server={proxy}')

    #driver = webdriver.Chrome()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    sleep(2)
    # It will help when someone the names are changed when minimized:
    # i.e Wednesday to WED
    driver.maximize_window()
    # implicit wait
    driver.implicitly_wait(10)

    driver.get(target_url)

    # Search for sign-in or login buttons
    #login_button = driver.find_elements(By.XPATH, "//*[contains(text(), 'Login')]")
    login_button = driver.find_elements(By.XPATH,
                                        "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'login') or "
                                        "contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'sign in')]")
    for btn in login_button:
        if btn.text.lower() == "login":
            btn.click()
            break

    provider_button = driver.find_elements(By.XPATH,
                                        "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'github') or "
                                        "contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'facebook')]")

    for btn in provider_button:
        if btn.text.lower() == "login":
            btn.click()
            break

# def main():
#     targets = ["https://.com/"]
#     for target in targets:
#         start_crawl(target)