import platform
import os

from user_interface import UI as interface


def clear_screen():
    if 'linux' in str(platform.platform()):
        clr = 'clear'
    else:
        clr = 'cls'
    os.system(clr)


if __name__ == '__main__':
    UI = interface()

    while True:
        clear_screen()
        UI.title()
        creds = UI.user_input()
        if creds == 'quit':
            clear_screen()
            exit()
