from logging import info

import click
from rich import print
from cli.commands import image
from cli.util import *

@image.command('classify', help='Classify a local image file using computer vision models.')
@click.option('--nsfw', 'model', flag_value='nsfw', default=True,  help='Use the nsfw model: https://github.com/GantMan/nsfw_model.')
@click.option('--nudenet', 'model', flag_value='nudenet', help='Use the NudeNet model: https://github.com/notAI-tech/NudeNet.')
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
        info(f'nudenet classification data for {filename}:')
        print(list(d.values())[0])
    
    else:
        exit_with_error(f'Unknown image classification model: {model}.')