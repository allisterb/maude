"""CLI interface for maude"""

import os
import sys
import threading
import warnings

import click

from logging import info, error, debug
from pyfiglet import Figlet
from rich import print

import maude_global

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Needs corresponding entry in PYTHONPATH or .env file
sys.path.append(os.path.join(maude_global.MAUDE_DIR, 'ext'))

def set_log_level(ctx, param, value):
    import logging
    from rich.logging import RichHandler
    if (value):
        logging.basicConfig(format='%(message)s', datefmt='%I:%M:%S %p', level=logging.DEBUG, handlers=[RichHandler(rich_tracebacks=True, show_path= True)])
        info("Debug mode enabled.")
    else:
        logging.basicConfig(format='%(message)s', datefmt='%I:%M:%S %p', level=logging.INFO, handlers=[RichHandler(rich_tracebacks=True, show_path=False)])
        #import tensorflow as tf
        #os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}  to control TensorFlow 2 logging level
        #tf.get_logger().setLevel('INFO')
        #tf.logging.set_verbosity(tf.logging.INFO)  # or any {DEBUG, INFO, WARN, ERROR, FATAL}

def print_logo():
    """Print program logo."""
    fig = Figlet(font='chunky')
    print('[cyan]' + fig.renderText('maud3') + '[/cyan]',  'v0.1' + os.linesep)
    
@click.group()
@click.option('--debug', is_flag=True, callback=set_log_level, expose_value=False)
def cli():
    print_logo()
    threading.Thread(target=maude_global.kb_capture_thread, args=(), name='kb_capture_thread', daemon=True).start()

@cli.group()
def classify(): pass

@classify.command('image')
@click.argument('model')
@click.argument('filename', type=click.Path(exists=True))
def classify_image(model, filename):
    if model == 'nfsw':
        from classifiers import nfsw_model
        c = nfsw_model.Classifier(filename, [])
    else:
        error('Unrecognized model', model)
        sys.exit(1)

if __name__ == '__main__': cli()

