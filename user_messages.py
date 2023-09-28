import threading
import sys
import time


class InfoMessages:
    def __init__(self):
        self.messages = {'login': 'Logging in with given credentials...\n',
                         'login_exists': 'Log-in credentials already exist...\n',
                         'cookies': 'Adding cookies to session...\n',
                         'saving': 'Saving cookies to file...\n',
                         'problems': 'Found Solved Problems...',
                         'observer': 'Fetching Links (Intersection Observer scrolling)...',
                         'container': 'Storing Links in list container...\n',
                         'links': 'Saving Links to file...\n',
                         'links_exist': 'Found links file...'}

    def invoke_and_animate_message(self, m_type):
        for i in self.messages[m_type]:
            time.sleep(0.02)
            print(end=i)
            time.sleep(0.02)

    def clear_terminal(self, m_type):
        for i in self.messages[m_type]:
            print(i, end='\r')
            time.sleep(0.02)

    def threaded_animation(self, message_type):
        t = threading.Thread(target=self.invoke_and_animate_message, args=(message_type,))
        t.start()
        t.join()
