"""CLI interface for maude"""

from ast import arg
import os
import sys
import threading
import warnings
import logging
from logging import info, error, debug
from pyfiglet import Figlet
#from ..ext.nsfw_model.nsfw_detector import predict
import kbinput
import click
from rich import print
from rich.logging import RichHandler
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

def set_log_level(ctx, param, value):
    if (value):
        logging.basicConfig(format='%(message)s', datefmt='%I:%M:%S %p', level=logging.DEBUG, handlers=[RichHandler(rich_tracebacks=True, show_path= True)])
        info("Debug mode enabled.")
    else:
        logging.basicConfig(format='%(message)s', datefmt='%I:%M:%S %p', level=logging.INFO, handlers=[RichHandler(rich_tracebacks=True, show_path=False)])

def print_logo():
    """Print program logo."""
    fig = Figlet(font='chunky')
    print('[cyan]' + fig.renderText('maude') + '[/cyan]',  'v0.1' + os.linesep)
    
@click.group()
@click.option('--debug', is_flag=True, callback=set_log_level, expose_value=False)
def cli():
    print_logo()
    threading.Thread(target=kbinput.kb_capture_thread, args=(), name='kb_capture_thread', daemon=True).start()

@cli.group()
def classify(): pass

@classify.command()
@click.argument('model')
def image(model):
    print(model)

if __name__ == '__main__':
    cli()

