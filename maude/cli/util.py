import os,sys
import click
from logging import info, error, warn, debug

import maude_global
def exception_handler(exc_type, exc, tb):
    from rich.console import Console
    from rich.traceback import Traceback
    console = Console(file=sys.stderr)
    console.print(
            Traceback.from_exception(
                exc_type,
                exc,
                tb,
                width=100,
                extra_lines=3,
                theme=None,
                word_wrap=False,
                show_locals=True if maude_global.DEBUG else False,
                indent_guides=True,
                suppress=([click]),
                max_frames=100,
            )
        )
def unhandled_exception_handler(ex_type, ex, tb):
    exception_handler(ex_type, ex, tb)
    error("A runtime exception occurred. maude will now exit.")
def exit_success():
    sys.exit(0)
    
def exit_if_dir_not_exists(path:str) -> str:
    if not os.path.exists(path):
        error(f'The directory {path} does not exist.')
        sys.exit(1)
    else:
        return path

def exit_if_file_not_exists(path:str) -> str:
    if not os.path.exists(path):
        error(f'The file {path} does not exist.')
        sys.exit(1)
    else:
        return path

def exit_with_error(msg:str):
    error(msg)
    sys.exit(1)