import os,sys
from logging import info, error, warn, debug
from typing import Any

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