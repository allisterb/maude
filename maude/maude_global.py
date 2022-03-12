import os

MAUDE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

KBINPUT = False

def kb_capture_thread():
    """Capture a keyboard input."""
    global KBINPUT
    input()
    #_ = getch.getch()
    KBINPUT = True