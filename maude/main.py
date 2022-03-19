"""CLI interface for maude"""
import os, sys
import threading
import warnings
from logging import error

from pyfiglet import Figlet
from rich import print

import maude_global
from base.runtime import exception_handler

# Needs corresponding entry in PYTHONPATH or .env file
sys.path.append(os.path.join(maude_global.MAUDE_DIR, 'ext'))

from pyipfs.ipfshttpclient.exceptions import VersionMismatch

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=VersionMismatch)

def unhandled_exception_handler(ex_type, ex, tb):
    exception_handler(ex_type, ex, tb)
    error('An runtime exception occurred. maude will now exit.')
         
sys.excepthook = unhandled_exception_handler

def print_logo():
    """Print program logo."""
    fig = Figlet(font='chunky')
    print('[cyan]' + fig.renderText('maud3') + '[/cyan]', '0.1' + os.linesep)
    
if __name__ == '__main__': 
    maude_global.INTERACTIVE_CLI = True
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0' if '--debug' in sys.argv[1:] else '3'
    print_logo()
    threading.Thread(target=maude_global.kb_capture_thread, args=(), name='kb_capture_thread', daemon=True).start()
    from cli.commands import parse
    parse()
    