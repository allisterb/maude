import sys
from logging import info, error

import click
from rich import print

from base.timer import begin
from cli.commands import binary

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

@yaracmd.command('analyze', help='Analyze an executable using a compiled YARA ruleset.')
@click.argument('filename', type=click.Path(exists=True))
@click.argument('ruleset', default='binaryalert')
def analyze(filename, ruleset):
    from binary.yara_classifier import Classifier
    c = Classifier(ruleset)
    print(c.classify(filename))

@binary.group('clamav', help='Run the ClamAV scanner.')
def clamavcmd():
    pass

@clamavcmd.command('info', help='Get info on ClamAV databases.')
def info():
    from binary.clamav_classifier import Classifier
    c = Classifier()
    print(c.get_info())

@clamavcmd.command('scan', help='Scan an executable or archive.')
@click.argument('filename', type=click.Path(exists=True))
def compile(filename):
    from binary.clamav_classifier import Classifier
    c = Classifier()
    print(c.classify(filename))
    