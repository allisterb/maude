"""CLI interface for maude"""

import os, sys
import threading
import warnings
from logging import info, error, debug

import click
from pyfiglet import Figlet
from rich import print

import maude_global
from cli_util import *

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Needs corresponding entry in PYTHONPATH or .env file
sys.path.append(os.path.join(maude_global.MAUDE_DIR, 'ext'))

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
                show_locals=True if maude_global.DEBUG else False,
                indent_guides=True,
                suppress=(),
                max_frames=100,
            )
        )
    error('An unhandled runtime exception occurred. Maude will now exit.')
         
sys.excepthook = unhandled_exception_handler

if maude_global.DEBUG:
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'  # or any {'0', '1', '2'}  to control TensorFlow 2 logging level
else:
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}  to control TensorFlow 2 logging level

def set_log_level(ctx, param, value):
    import logging
    from rich.logging import RichHandler
    from cli_logging import MaudeHighlighter
    if (value):
        maude_global.DEBUG = True
        logging.basicConfig(format='%(message)s', datefmt='%I:%M:%S %p', level=logging.DEBUG, handlers=[RichHandler(rich_tracebacks=True, highlighter = MaudeHighlighter(), show_path= True)])
        info("Debug mode enabled.")
    else:
        logging.basicConfig(format='%(message)s', datefmt='%I:%M:%S %p', level=logging.INFO, handlers=[RichHandler(rich_tracebacks=True, highlighter = MaudeHighlighter(), show_path=False)])

def print_logo():
    """Print program logo."""
    fig = Figlet(font='chunky')
    print('[cyan]' + fig.renderText('maud3') + '[/cyan]', '0.1' + os.linesep)
    
# Command-line argument handling starts here
@click.group()
@click.option('--debug', is_flag=True, callback=set_log_level, expose_value=False)
def cli():
    print_logo()
    threading.Thread(target=maude_global.kb_capture_thread, args=(), name='kb_capture_thread', daemon=True).start()

@cli.group()
def image(): pass

@cli.group()
def text(): pass

@image.command('classify')
@click.argument('model')
@click.argument('filename', type=click.Path(exists=True))
def image_classify(model, filename):
    if model == 'nfsw':
        from image.nfsw_classifier import Classifier
        nfsw = Classifier(filename, [])
        d = nfsw.classify()
        print(d)
    else:
        error('Unknown model: %s', model)
        sys.exit(1)

@text.command('similarity')
@click.argument('model', default='spacy')
@click.argument('sentence1')
@click.argument('sentence2')
def text_similarity(model, sentence1, sentence2):
    if model == 'spacy':
        from text.spacy_similarity import TextSimilarity
        spacy = TextSimilarity()
        print(spacy.similarity(sentence1, sentence2))
    else:
        exit_with_error(f'Unknown model: {model}.')

if __name__ == '__main__': cli()