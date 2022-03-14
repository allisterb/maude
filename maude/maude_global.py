import os
from logging import info

DEBUG = False

MAUDE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

KBINPUT = False

def kb_capture_thread():
    """Capture a keyboard input."""
    global KBINPUT
    input()
    info("Enter key pressed...")
    #_ = getch.getch()
    KBINPUT = True