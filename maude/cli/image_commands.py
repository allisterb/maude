from logging import info

import click
from rich import print
from cli.commands import image
from cli.util import *

@image.command('classify')
@click.argument('model')
@click.argument('filename', type=click.Path(exists=True))
def image_classify(model, filename):
    if model == 'nsfw':
        from image.nfsw_classifier import Classifier
        nfsw = Classifier()
        d = nfsw.classify(filename)
        info(f'nfsw classification data for {filename}:')
        print(list(d.values())[0])
    
    elif model == 'nudenet':
        from image.nudenet_classifier import Classifier
        nn = Classifier()
        d = nn.classify(filename)
        print(list(d.values())[0])
    
    else:
        exit_with_error(f'Unknown image classification model: {model}.')
        