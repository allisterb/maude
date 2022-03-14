import click

from cli.commands import text
from cli.util import *

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