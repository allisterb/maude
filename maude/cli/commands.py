import threading
from logging import info

from pyfiglet import Figlet
import click

from cli.maude_logging import set_log_level
from cli.util import *
    
@click.group()
@click.option('--debug', is_flag=True, callback=set_log_level, expose_value=False)
def parse(): pass
    
@parse.group()
def image(): pass

@parse.group()
def text(): pass

@parse.group('import')
def data_import(): pass

@image.command('classify')
@click.argument('model')
@click.argument('filename', type=click.Path(exists=True))
def image_classify(model, filename):
    if model == 'nfsw':
        from image.nfsw_classifier import Classifier
        nfsw = Classifier(filename, [])
        d = nfsw.classify()
        print(d)
    else:
        error('Unknown model: %s', model)
        sys.exit(1)

@text.command('similarity')
@click.argument('model', default='spacy')
@click.argument('sentence1')
@click.argument('sentence2')
def text_similarity(model, sentence1, sentence2):
    if model == 'spacy':
        from text.spacy_similarity import TextSimilarity
        spacy = TextSimilarity()
        print(spacy.similarity(sentence1, sentence2))
    else:
        exit_with_error(f'Unknown model: {model}.')

@data_import.command('reddit')
@click.argument('client_id', envvar='MAUDE_REDDIT_CLIENT_ID')
@click.argument('client_secret', envvar='MAUDE_REDDIT_CLIENT_SECRET')
@click.argument('client_user', envvar='MAUDE_REDDIT_CLIENT_USER')
@click.argument('client_pass', envvar='MAUDE_REDDIT_CLIENT_PASS')
def data_import_reddit(client_id, client_secret, client_user, client_pass):
   from data.reddit_data_importer import DataImporter
   importer = DataImporter(client_id, client_secret, client_user, client_pass)