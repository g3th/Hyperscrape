import os
from pathlib import Path
from user_messages import InfoMessages
from browser_init import check_if_problems_file_exists, ReturnNumberOfSolvedProblems
from browser_init import BrowserInit, check_if_cookie_file_exists
from cookies import ObtainCookie
from scraper import Scraper


class UI:

    def __init__(self):
        self.page = 'https://hyperskill.org/comments?threads=solutions&custom=myComments,completedOnly'
        self.error = False
        self.browser_window_size = [200, 300]
        self.headless = ' - [Off]'
        self.spaces = ' ' * 28 + '|'
        self.messages = InfoMessages()
        self.credentials = []
        self.is_task = False
        self.user_options = ''

    def title(self):
        print('''\033[38;5;38m██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗ ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗
\033[38;5;74m██║  ██║╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝
\033[38;5;110m███████║ ╚████╔╝ ██████╔╝█████╗  ██████╔╝███████╗██║     ██████╔╝███████║██████╔╝█████╗  
\033[38;5;74m██╔══██║  ╚██╔╝  ██╔═══╝ ██╔══╝  ██╔══██╗╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  
\033[38;5;38m██║  ██║   ██║   ██║     ███████╗██║  ██║███████║╚██████╗██║  ██║██║  ██║██║     ███████╗
\033[38;5;38m╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝
----------------------------------------------------------------------------------------
                          A simple scraper for Hyperskill                                                                                         
----------------------------- https://github.com/g3th ----------------------------------''')
        print("\nPick Option:")
        print("+-----------------------------------------------------+")
        print('| 1. Login                                            |')
        print('| 2. Download Completed Problems                      |')
        print('| 3. Headless Mode' + self.headless + self.spaces)
        print('| 4. Set Browser Window Size (Headless Off)           |')
        print('| 5. Download Completed Problems Theory (coming soon) |')
        print('| 6. Quit                                             |')
        print("+-----------------------------------------------------+")

    def user_input(self):

        self.user_options = input("> ")
        match self.user_options:
            case "1":
                file_exists = False
                while True:
                    for i in os.listdir('credentials'):
                        if 'creds.txt' in i and os.path.getsize(str(Path(__file__).parent) + '/credentials/' + i) != 0:
                            self.messages.threaded_animation('login_exists')
                            input("Press Enter to Continue.")
                            file_exists = True
                            with open('credentials/creds.txt', 'r') as creds:
                                for j in creds.readlines():
                                    self.credentials.append(j + "\n")
                    if file_exists:
                        break
                    else:
                        print("Enter your Hyperskill credentials:")
                        email = input("Email: ")
                        password = input("Password: ")
                        self.credentials = [email, password]
                        with open('credentials/creds.txt', 'w') as creds:
                            for k in self.credentials:
                                creds.write(k + "\n")
                            break
                # Login
                # Create a persistent session
                # open browser - add cookies - refresh browser
                ObtainCookie().login()

            case "2":
                selenium = BrowserInit(self.headless, self.browser_window_size[0], self.browser_window_size[1])
                scrape = Scraper(selenium.browser)
                try:
                    selenium.fetch_page('https://hyperskill.org/', 5)
                    ObtainCookie().open_cookies(selenium.browser)
                    selenium.fetch_page('https://hyperskill.org/', 5)
                    selenium.fetch_page(self.page, 5)
                except FileNotFoundError:
                    print("Cookies not found")
                    print("Please login.")
                    input("Press Enter to continue.")
                if not check_if_problems_file_exists():
                    total_number_of_solved_problems = ReturnNumberOfSolvedProblems(selenium.browser)
                    total_number_of_solved_problems.return_number_of_solved_problems()
                    total_number_of_solved_problems.write_number_of_problems_to_file()
                    open_file = open('Total_Number_Of_Problems', 'r').readline()
                    number_of_problems = open_file.split(" ")[0]
                else:
                    open_file = open('Total_Number_Of_Problems', 'r').readline()
                    print(" - (" + open_file.split(" ")[0] + " Solutions)\n")
                    number_of_problems = open_file.split(" ")[0]
                self.messages.threaded_animation('problems')
                print("(Total - )" + number_of_problems + "\n")
                scrape.threaded_link_scraper(int(number_of_problems))
                links_list = []
                with open('Problem_Links.txt', 'r') as problem_links:
                    for i in problem_links.readlines():
                        links_list.append(i)
                index = 0
                while index != len(links_list):
                    self.is_task = False
                    if 'projects' in str(links_list[index]):
                        self.is_task = True
                    selenium.fetch_page(links_list[index].strip(), 10)
                    scrape.code_scraper(self.is_task)
                    scrape.save_code_file()
                    index += 1
            case "3":
                if self.headless == ' - [Off]':
                    self.headless = ' - [On]'
                    self.spaces = ' ' * 29 + '|'
                else:
                    self.headless = ' - [Off]'
                    self.spaces = ' ' * 28 + '|'
            case "4":
                values = input("Enter width and height values (i.e. 200 200):")
                self.browser_window_size.append(int(values.split(" ")[0]))
                self.browser_window_size.append(int(values.split(" ")[1]))
            case "5":
                print("Coming Soon!")
                input("Press Enter to Continue...")
            case "6":
                return 'quit'
            case _:
                print("Invalid Option")
                input("Press Enter to Continue...")