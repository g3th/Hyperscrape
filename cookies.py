import json
import time
from user_messages import InfoMessages
from selenium.webdriver.common.by import By
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class ObtainCookie:

    def __init__(self):
        self.sign_in = 'https://hyperskill.org/login'
        self.user_directory = str(Path(__file__).parent)
        self.messages = InfoMessages()
        self.browser_options = Options()
        self.browser_options.add_argument('--headless==new')
        self.browser = webdriver.Chrome(options=self.browser_options)
        self.credentials = []

    def login(self):
        self.messages.threaded_animation('login')
        creds = open(self.user_directory + '/credentials/creds.txt', 'r')
        for i in creds.readlines():
            self.credentials.append(i)
        self.browser.get(self.sign_in)
        user = self.browser.find_element(By.XPATH, '/html/body/div/main/div/div/div[2]/div/form/fieldset[1]/div/input')
        password = self.browser.find_element(By.XPATH,
                                             '/html/body/div/main/div/div/div[2]/div/form/fieldset[2]/div/input')
        sign_in_button = self.browser.find_element(By.XPATH, '/html/body/div/main/div/div/div[2]/div/form/button')
        user.send_keys(self.credentials[0])
        password.send_keys(self.credentials[1])
        sign_in_button.click()
        self.messages.threaded_animation('login')
        time.sleep(5)
        self.messages.threaded_animation('saving')
        self.browser.get('https://hyperskill.org/comments')
        time.sleep(2)
        with open(self.user_directory + '\cookie.json', 'w') as write_cookie:
            json.dump(self.browser.get_cookies(), write_cookie, indent=3)

    def open_cookies(self, main_browser):
        self.messages.threaded_animation('cookies')
        with open(self.user_directory + '\cookie.json', 'r') as read_cookie:
            opened_jar = json.load(read_cookie)
            for cookie in opened_jar:
                main_browser.add_cookie(cookie)
        read_cookie.close()

