PADDING = 20

RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
YELLOW = "\033[33m"
WHITE = "\033[37m"

REVERSE = "\033[;7m" # Reverses colors in CLI
RESET = "\033[0m"   # Resets color back to default

def change_color(color):
    print(color, end="")