import sys
from logging import info, error

import click
from rich import print
from numpy import dot
from numpy.linalg import norm

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

@image.group(help='Generate Mod2Vec sentences and sentence vectors from images.')
def mod2vec(): pass

@mod2vec.command('print', help='Generate a Mod2Vec sentence and sentence vector from an image.')
@click.argument('filename', type=click.Path(exists=True))
@click.option('--spacy', 'embedding', flag_value='spacy', default=True,  help='Use the default spaCy sentence embedding.')
@click.option('--use', 'embedding', flag_value='use', help='Use Google universal sentence encoder.')
def _print(filename, embedding):
    from image.nfsw_classifier import Classifier as NsfwClassifier
    nsfw = NsfwClassifier()
    from image.nudenet_classifier import Classifier as NudeNetClassifier
    nn = NudeNetClassifier()
    from core.mod2vec import image_mod2vec
    file_analysis = dict()
    file_analysis['image'] = {**nn.classify(filename), **nsfw.classify(filename)}
    info(f'Classification data for image {filename}:')
    print(file_analysis["image"])
    se = None
    if embedding == 'spacy':
        from text.spacy_embedding import WordAverageEmbedding as spaCyEmbedding
        se = spaCyEmbedding()
    elif embedding == 'use':
        from text.spacy_embedding import UseEmbedding as spaCyEmbedding
        se = spaCyEmbedding()
    else:
        error(f'Invalid sentence embedding: {embedding}.')
    s, vec = image_mod2vec(file_analysis["image"], se)
    info(f'Mod2Vec: {s}')
    print(vec)

@mod2vec.command(help='Generate a Mod2Vec sentence and sentence vector from an image.')
@click.argument('filename1', type=click.Path(exists=True))
@click.argument('filename2', type=click.Path(exists=True))
@click.option('--spacy', 'embedding', flag_value='spacy', help='Use the default spaCy sentence embedding.')
@click.option('--use', 'embedding', flag_value='use', default=True, help='Use the spaCy universal sentence encoder.')
def compare(filename1, filename2, embedding):
    from image.nfsw_classifier import Classifier as NsfwClassifier
    nsfw = NsfwClassifier()
    from image.nudenet_classifier import Classifier as NudeNetClassifier
    nn = NudeNetClassifier()
    from core.mod2vec import image_mod2vec
    se = None
    if embedding == 'spacy':
        from text.spacy_embedding import WordAverageEmbedding as spaCyEmbedding
        se = spaCyEmbedding()
    elif embedding == 'use':
        from text.spacy_embedding import UseEmbedding as spaCyEmbedding
        se = spaCyEmbedding()
    else:
        error(f'Invalid sentence embedding: {embedding}.')
    file_analysis1 = dict()
    file_analysis1['image'] = {**nn.classify(filename1), **nsfw.classify(filename1)}
    info(f'Classification data for image {filename1}:')
    print(file_analysis1["image"])
    file_analysis2 = dict()
    file_analysis2['image'] = {**nn.classify(filename2), **nsfw.classify(filename2)}
    info(f'Classification data for image {filename2}:')
    print(file_analysis2["image"])
    s1, vec1 = image_mod2vec(file_analysis1["image"], se)
    s2, vec2 = image_mod2vec(file_analysis2["image"], se)
    similarity = dot(vec1, vec2) / (norm(vec1) * norm(vec2))
    info(f'Mod2Vec comparison of {filename1} and {filename2}:')
    info(f'1. {s1}')
    info(f'2. {s2}')
    info(f'Similarity: {similarity}.')
