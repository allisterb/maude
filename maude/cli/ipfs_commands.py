import click
from rich import print

from cli.commands import ipfs
from cli.util import *
from core.ipfs import get_client_id

@ipfs.command('info')
def ipfs_info():
    print(get_client_id())
