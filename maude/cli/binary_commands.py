import sys
from logging import info, error

import click
from rich import print

from base.timer import begin
from cli.commands import binary
from cli.util import exit_with_error

@binary.group('yara', help='Run YARA rules on an executable.')
def yaracmd():
    pass
    
@yaracmd.command('compile', help='Compile YARA rules in a directory into a single file.')
@click.argument('rules-dir', type=click.Path(exists=True))
@click.argument('output-file', type=click.Path(exists=False))
def compile(rules_dir, output_file):
    from binary.yara_classifier import compile_rules
    with begin(f'Compiling YARA rules in {rules_dir} to {output_file}') as op:
        compile_rules(rules_dir, output_file)
        op.complete()