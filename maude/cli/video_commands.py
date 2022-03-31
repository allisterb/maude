import json
from logging import info

import click
from rich import print
from cli.commands import video
from cli.util import *

@video.command('classify', help='Classify a local video file using computer vision models.')
@click.option('--nudenet', 'model', flag_value='nudenet', default=True, help='Use the NudeNet model: https://github.com/notAI-tech/NudeNet.')
@click.argument('filename', type=click.Path(exists=True))
def video_classify(model, filename):
    if model == 'nudenet':
        from video.nudenet_classifier import Classifier
        nn = Classifier()
        cd = nn.classify(filename)
        #dd = nn.detect_objects(filename)
        #data = list(cd.values())[0] 
        #data['objects'] = dd  
        info(f'NudeNet classification and detection data for {filename}:')
        print(cd)
    else:
        exit_with_error(f'Unknown video classification model: {model}.')