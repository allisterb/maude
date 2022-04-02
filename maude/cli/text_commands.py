import click

from rich import print
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

@text.command('perspective', help='Classify a sentence using Google Perspective API.')
@click.option('--experimental', is_flag=True, default=False, help='Use experimental Perspective attributes.')
@click.argument('sentence')
@click.argument('perspective_api_key', envvar='PERSPECTIVE_API_KEY')
def text_similarity(perspective_api_key, experimental, sentence):
        import text.perspective_classifier
        text.perspective_classifier.api_key = perspective_api_key
        perspective_classifier = text.perspective_classifier.TextClassifier()
        info(f'Google Perspective API key is {perspective_api_key[0:2]}...')
        print(perspective_classifier.classify(sentence, experimental))
