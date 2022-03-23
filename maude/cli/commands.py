import click

from cli.logging import set_log_level
    
@click.group()
@click.option('--debug', is_flag=True, callback=set_log_level, expose_value=False)
def parse(): pass
    
@parse.group()
def image(): pass

@parse.group()
def text(): pass

@parse.group('import')
def data_import(): pass

@parse.group()
def crypto():
    pass

@parse.group()
def ipfs():
    pass

@parse.group()
def server():
    pass

import cli.image_commands
import cli.text_commands
import cli.data_import_commands
import cli.crypto_commands
import cli.ipfs_commands
import cli.server_commands