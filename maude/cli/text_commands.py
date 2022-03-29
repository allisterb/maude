import click

from cli.commands import text
from cli.util import *

@text.command('similarity', help='Calculate the similarity of two sentences using an NLU model.')
@click.option('--spacy', 'model', flag_value='spacy', default=True, help='Use the spaCy NLU model.')
@click.argument('sentence1')
@click.argument('sentence2')
def text_similarity(model, sentence1, sentence2):
    if model == 'spacy':
        from text.spacy_similarity import TextSimilarity
        spacy = TextSimilarity()
        info(f'Similarity: {spacy.similarity(sentence1, sentence2)}.')
    else:
        exit_with_error(f'Unknown NLP model: {model}.')