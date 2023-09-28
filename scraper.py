import time
import concurrent.futures
import os
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from user_messages import InfoMessages


class Scraper:

    def __init__(self, browser):
        self.is_task = False
        self.problem_title = ''
        self.problem_stage = ''
        self.code = ''
        self.messages = InfoMessages()
        self.browser = browser
        self.solved_problem_links_list = []
        self.lazy_loading_images_increment = 11

    # Lazy Loading scroller, to fill the page with all existing solution links.
    def lazy_load_all_problems(self):
        while self.browser.find_elements(By.XPATH, '/html/body/div/main/div/div/div/div[2]/div/div/div[' +
                                                   str(self.lazy_loading_images_increment) + ']'):
            self.messages.threaded_animation('observer')
            observer_element = self.browser.find_element(By.XPATH, '/html/body/div/main/div/div/div/div[2]/div/div/div['
                                                         + str(self.lazy_loading_images_increment) + ']')
            self.browser.execute_script("arguments[0].scrollIntoView(true);", observer_element)
            time.sleep(4)
            self.lazy_loading_images_increment += 10
            self.messages.clear_terminal('observer')
    # Function which returns a single link only
    # Used with ThreadPoolExecutor
    def problem_links(self, i):
        while self.browser.find_elements(By.XPATH, '/html/body/div/main/div/div/div/div[2]/div/div/div['
                                                   + str(i) +
                                                   ']/div[2]/div/div[2]/a'):
            current_xpath = self.browser.find_element(By.XPATH, '/html/body/div/main/div/div/div/div[2]/div/div/div['
                                                      + str(i) +
                                                      ']/div[2]/div/div[2]/a')
            current_link = current_xpath.get_attribute('href')
            return current_link

    # Fetches all the links for the solution pages in parallel, with threads.
    def threaded_link_scraper(self, number_of_problems):
        urls = []
        for k in os.listdir():
            if 'Problem_Links' in k:
                self.messages.threaded_animation('links_exist')
                with open('Problem_Links.txt', 'r') as problems:
                    for i in problems.readlines():
                        urls.append(i)
                problems.close()
                return urls
        futures_list = []
        self.lazy_load_all_problems()
        self.messages.threaded_animation('container')
        with concurrent.futures.ThreadPoolExecutor(10) as executor:
            for i in range(number_of_problems):
                thread = executor.submit(self.problem_links, i)
                futures_list.append(thread)
            for j in futures_list:
                result = j.result()
                if result is not None:
                    urls.append(result)
        self.write_problem_links_to_file(urls)
        executor.shutdown()
    # Write scraped links into text file, so they are retrievable in the next session
    def write_problem_links_to_file(self, result):
        self.messages.threaded_animation('links')
        with open('Problem_Links.txt', 'w') as links:
            for link in result:
                links.write(link + "\n")
        links.close()

    def code_scraper(self, is_task):
        self.is_task = is_task
        # The Link is not just a problem, but it's a task with Stages
        # A task is an entire project essential towards completing 'tracks'
        if self.is_task:
            self.problem_stage = self.browser.find_element(By.CSS_SELECTOR, '#step__header > div > h2').text
            self.problem_title = self.browser.find_element(By.XPATH, '/html/body/div/main/div/div/div[1]/div['
                                                                     '1]/div/span').text
            problem_desc = self.browser.find_element(By.XPATH, '/html/body/div/main/div/div/div[1]/div[2]/div/div['
                                                               '1]/div[1]').text
            self.code = self.browser.find_element(By.XPATH, '/html/body/div/main/div/div/div[1]/div[5]/div/div/div['
                                                            '5]/div/div[3]/div/div[2]/div/div/div[2]/div/div['
                                                            '2]/pre/code').text
            with open('code/README.MD', 'a', encoding='utf-8') as code:
                code.write(self.problem_title.capitalize() +
                           "\n-----------------------------\n" +
                           self.problem_stage +
                           "\n------------------------------\n" +
                           problem_desc)
            code.close()
        # The link is a normal problem, such as a 'daily problem' or quiz
        else:
            self.problem_title = self.browser.find_element(By.CSS_SELECTOR, '#step-title').text
            problem_desc = self.browser.find_element(By.XPATH, '/html/body/div/main/div/div/div/div/div[2]/div/div[1]/div['
                                                               '1]/div[2]').text
            self.code = self.browser.find_element(By.XPATH, '/html/body/div/main/div/div/div/div/div[5]/div/div/div['
                                                            '5]/div/div[3]/div/div[2]/div/div/div[1]/div/div['
                                                            '2]/div').text
            with open('code/README.MD', 'a', encoding='utf-8') as code:
                code.write(self.problem_title.capitalize() +
                           "\n-----------------------------\n" +
                           problem_desc +
                           "\n------------------------------\n")
            code.close()


    def save_code_file(self):
        if self.is_task:
            title = self.problem_title.split(":")[1] + "_" + self.problem_stage.split(" ")[3].replace("/", " out of ")
            self.problem_title = title
        with open('code/' + self.problem_title + ".kt", 'w', encoding='utf-8') as save_problem_file:
            save_problem_file.write(self.code)
        save_problem_file.close()
