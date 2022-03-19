import os
from logging import info

DEBUG = False

MAUDE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

KBINPUT = False

INTERACTIVE_CLI = False

def kb_capture_thread():
    """Capture keyboard input"""
    global KBINPUT
    try:
        input()
        info("Enter key pressed...")
        #_ = getch.getch()
        KBINPUT = True
    except EOFError as _:
        info('Ctrl-C pressed...')
        KBINPUT = True
        if INTERACTIVE_CLI:
            info('Stop requested.')