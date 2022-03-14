from logging import info, error, warn, debug

import click

from cli.logging import set_log_level
from cli.util import exit_with_error
    
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
        exit_with_error(f'Unknown image classification model: {model}.')
        
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
        exit_with_error(f'Unknown NLP model: {model}.')

@data_import.command('reddit')
@click.argument('subreddit', required = True)
@click.argument('sort', required = False, type=click.Choice(['hot', 'top', 'new'], case_sensitive=False), default = 'hot')
@click.argument('submission_limit', required = False, type=int, default = 100)
@click.argument('comment_limit', required = False, type=int, default = 1000)
@click.argument('time_filter', required = False, type=click.Choice(['hour', 'year', 'all', 'week', 'month', 'day'], case_sensitive=False), default = 'all')
@click.argument('client_id', envvar='MAUDE_REDDIT_CLIENT_ID')
@click.argument('client_secret', envvar='MAUDE_REDDIT_CLIENT_SECRET')
@click.argument('client_user', envvar='MAUDE_REDDIT_CLIENT_USER')
@click.argument('client_pass', envvar='MAUDE_REDDIT_CLIENT_PASS')
def data_import_reddit(subreddit, sort, submission_limit, comment_limit, time_filter, client_id, client_secret, client_user, client_pass):
   from data.reddit_data_importer import DataImporter
   importer = DataImporter(client_id, client_secret, client_user, client_pass)
   importer.import_data(subreddit, sort, submission_limit, comment_limit, time_filter)