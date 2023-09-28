import time
import os
from user_messages import InfoMessages
from pathlib import Path
from cookies import ObtainCookie
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By


class BrowserInit:
    # Webdriver initialization:
    # Headless on/off, user agent and cookies for persistent session
    def __init__(self, headless, w, h):
        self.info_message = InfoMessages()
        self.obtain_cookie = ObtainCookie()
        self.browser_options = Options()
        self.browser_options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                          '(KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"')
        if headless == ' - [On]':
            self.browser_options.add_argument('--headless==new')
        self.browser = webdriver.Chrome(options=self.browser_options)
        self.browser.set_window_size(w, h)

    # Do cookies exist, in the form of a json file? If not, return 1
    def check_cookies(self):
        try:
            self.obtain_cookie.login()
            time.sleep(2)
        except FileNotFoundError:
            return 1

    def fetch_page(self, web_page, wait):
        self.browser.get(web_page)
        time.sleep(wait)

    def close_browser(self):
        self.browser.quit()


def check_if_problems_file_exists():
    for i in os.listdir():
        if 'Total_Number_Of_Problems' in str(i):
            return True


def check_if_cookie_file_exists():
    for i in os.listdir():
        if 'cookies.json' in str(i):
            return True


class ReturnNumberOfSolvedProblems:

    def __init__(self, browser):
        self.browser = browser
        self.directory = str(Path(__file__).parent)
        self.number_of_problems = ''

    def return_number_of_solved_problems(self):
        drop_down = self.browser.find_element(By.XPATH, '/html/body/div/header/nav/div/div[2]/li[2]/a')
        drop_down.click()
        time.sleep(2)
        profile = self.browser.find_element(By.XPATH, '/html/body/div/header/nav/div/div[2]/li[2]/ul/li[1]/a')
        profile.click()
        time.sleep(2)
        self.number_of_problems = self.browser.find_element(By.XPATH, '/html/body/div/main/div/div/div/div[2]/div['
                                                                      '4]/div/section[3]/div/div[2]/div/div[4]').text

    def write_number_of_problems_to_file(self):
        with open('Total_Number_Of_Problems', 'w') as mo_money:
            mo_money.write(self.number_of_problems)
        mo_money.close()
