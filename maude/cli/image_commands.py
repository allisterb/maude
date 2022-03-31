import sys
from logging import info, error

import click
from rich import print

from cli.commands import image
from cli.util import exit_with_error

@image.command('classify', help='Classify a local image file using computer vision models.')
@click.option('--nsfw', 'model', flag_value='nsfw', default=True,  help='Use the nsfw model: https://github.com/GantMan/nsfw_model.')
@click.option('--nudenet', 'model', flag_value='nudenet', help='Use the NudeNet model: https://github.com/notAI-tech/NudeNet.')
@click.argument('filename', type=click.Path(exists=True))
def image_classify(model, filename):
    if model == 'nsfw':
        from image.nfsw_classifier import Classifier
        nfsw = Classifier()
        info(f'nfsw_model classification data for {filename}:')
        print(nfsw.classify(filename))
    
    elif model == 'nudenet':
        from image.nudenet_classifier import Classifier
        nn = Classifier()
        info(f'NudeNet classification and detection data for {filename}:')
        print(nn.classify(filename))
    
    else:
        exit_with_error(f'Unknown image classification model: {model}.')

@image.command('photodna', help='Generate a Microsoft PhotoDNA hash of a local image file.')
@click.option('--libpath', default=None, help='The path to the Microsoft PhotoDNA library, or omit to use the default path. See: https://github.com/jankais3r/pyPhotoDNA.')
@click.argument('filename', type=click.Path(exists=True))
def photodna_hash(libpath, filename,):
    if not ((sys.platform == "win32") or (sys.platform == "darwin")):
        exit_with_error('Microsoft PhotoDNA is only supported on Windows and macOS.')
    from image.ms_photodna import generateHash
    print(f'Microsoft PhotoDNA hash of {filename} is {generateHash(filename, libpath)}')

