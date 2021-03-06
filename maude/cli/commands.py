import click

from cli.logging import set_log_level
    
@click.group()
@click.option('--debug', is_flag=True, callback=set_log_level, expose_value=False)
def parse(): pass

@parse.group(help  = 'Run malware detection and other rules on binary files.')
def binary(): pass

@parse.group(help  = 'Run computer vision ML models and algorithms on local image files.')
def image(): pass

@parse.group(help  = 'Run computer vision ML models on local video files.')
def video(): pass

@parse.group(help  = 'Run NLU ML models on specified text.')
def text(): pass

@parse.group('import', help  = 'Import training data from specified data.')
def data_import(): pass

@parse.group(help  = 'Run public-key cryptography tasks.')
def crypto(): pass

@parse.group(help  = 'Run commands on an IPFS node.')
def ipfs(): pass

@parse.group(help  = 'Start the maude server.')
def server(): pass

import cli.binary_commands
import cli.image_commands
import cli.video_commands
import cli.text_commands
import cli.data_import_commands
import cli.crypto_commands
import cli.ipfs_commands
import cli.server_commands