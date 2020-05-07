# colors 
class bcolors:
    def __init__(self):
        self.HEADER = '\033[95m'
        self.OKBLUE = '\033[94m'
        self.OKGREEN = '\033[92m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'
        self.BOLD = '\033[1m'
        self.ITALIC = '\033[3m'
        self.UNDERLINE = '\033[4m'
        self.CYAN = '\033[96m'

        self.colors = {
            'blue': self.OKBLUE,
            'green': self.OKGREEN,
            'red': self.FAIL,
            'yellow': self.WARNING,
            'header': self.HEADER,
            'italic': self.ITALIC,
            'cyan': self.CYAN,
            'bold': self.BOLD,
            'underline': self.UNDERLINE
        }
    
    def get_color(self, color, text):
        return self.colors[color] + text + self.ENDC

bcolor = bcolors()
