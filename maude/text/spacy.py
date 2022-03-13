import spacy
from timer import begin

nlp = None

with begin('Loading spaCy model en_core_web_lg') as op:
    nlp = spacy.load("en_core_web_lg")
    op.complete()