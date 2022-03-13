"""CLI interface for maude"""

import os, sys
import threading
import warnings
from logging import info, error, debug

from pyfiglet import Figlet
from rich import print

from maude_global import DEBUG, MAUDE_DIR, kb_capture_thread

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Needs corresponding entry in PYTHONPATH or .env file
sys.path.append(os.path.join(MAUDE_DIR, 'ext'))

def unhandled_exception_handler(exctype, value, tb):
    from rich.console import Console
    from rich.traceback import Traceback
    console = Console(file=sys.stderr)
    console.print(
            Traceback.from_exception(
                exctype,
                value,
                tb,
                width=100,
                extra_lines=3,
                theme=None,
                word_wrap=False,
                show_locals=True if DEBUG else False,
                indent_guides=True,
                suppress=(),
                max_frames=100,
            )
        )
    error('An unhandled runtime exception occurred. Maude will now exit.')
         
sys.excepthook = unhandled_exception_handler

if DEBUG:
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'  # or any {'0', '1', '2'}  to control TensorFlow 2 logging level
else:
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}  to control TensorFlow 2 logging level

def print_logo():
    """Print program logo."""
    fig = Figlet(font='chunky')
    print('[cyan]' + fig.renderText('maud3') + '[/cyan]', '0.1' + os.linesep)
    
if __name__ == '__main__': 
    print_logo()
    threading.Thread(target=kb_capture_thread, args=(), name='kb_capture_thread', daemon=True).start()
    
    # Command-line argument handling starts here
    from cli.commands import cli
    cli()
    