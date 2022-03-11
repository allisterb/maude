"""CLI interface for TrafficCV"""

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
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

def print_logo():
    """Print program logo."""
    fig = Figlet(font='chunky')
    print(fig.renderText('maude') + 'v0.1\n')
    
    
@click.command()
@click.option('--debug', is_flag=True)
def cli(debug):
    if (debug):
        logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%I:%M:%S %p', level=logging.DEBUG)
        info("Debug mode enabled.")
    else:
        logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%I:%M:%S %p', level=logging.INFO)
    print_logo()
    threading.Thread(target=kbinput.kb_capture_thread, args=(), name='kb_capture_thread', daemon=True).start()

if __name__ == '__main__':
    cli()
