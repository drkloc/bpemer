from colorama import Fore, Back, Style

class SimpleLine(object):
    def __init__(self, text, color=Fore.WHITE, background=Back.BLACK):
        print
        print(background + color + ' ' + text + ' ' + Style.RESET_ALL)
        print
