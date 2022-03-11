"""CLI interface for maude"""

import os
import sys
import threading
import warnings
import logging
from logging import info, error, debug
from pyfiglet import Figlet
#from ..ext.nsfw_model.nsfw_detector import predict
from colorama import Fore, Back, Style
import kbinput
import click
from rich import print
from rich.logging import RichHandler
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

def print_logo():
    """Print program logo."""
    fig = Figlet(font='chunky')
    print('[cyan]' + fig.renderText('maude') + '[/cyan]',  'v0.1' + os.linesep)
    
@click.command()
@click.option('--debug', is_flag=True)
def cli(debug):
    if (debug):
        logging.basicConfig(format='%(message)s', datefmt='%I:%M:%S %p', level=logging.DEBUG, handlers=[RichHandler(rich_tracebacks=True, show_path= True)])
        info("Debug mode enabled.")
    else:
        logging.basicConfig(format='%(message)s', datefmt='%I:%M:%S %p', level=logging.INFO, handlers=[RichHandler(rich_tracebacks=True, show_path=False)])
        info("Debug mode not enabled.")
    
    print_logo()
    
    threading.Thread(target=kbinput.kb_capture_thread, args=(), name='kb_capture_thread', daemon=True).start()

if __name__ == '__main__':
    cli()
