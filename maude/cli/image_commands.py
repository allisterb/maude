import click

from cli.commands import image
from cli.util import *

@image.command('classify')
@click.argument('model')
@click.argument('filename', type=click.Path(exists=True))
def image_classify(model, filename):
    if model == 'nsfw':
        from image.nfsw_classifier import Classifier
        nfsw = Classifier(filename, [])
        d = nfsw.classify()
        print(d)
    else:
        exit_with_error(f'Unknown image classification model: {model}.')
        