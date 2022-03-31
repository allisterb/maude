import sys
from logging import info, error

import click
from rich import print

from cli.commands import binary
from cli.util import exit_with_error

@binary.command('yara', help='Run YARA rules on an executable.')
@click.option('--def', 'ruleset', flag_value='nsfw', default=True,  help='Use the nsfw model: https://github.com/GantMan/nsfw_model.')
@click.argument('filename', type=click.Path(exists=True))
def yara(ruleset, filename):
    from binary.yara_classifier import Classifier
    c = Classifier()
    
