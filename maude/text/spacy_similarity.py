import os, sys

from text.spacy import nlp
from timer import begin

from logging import info, error, warn, debug
from text_similarity import TextSimilarity

class TextSimilarity(TextSimilarity):
    def __init__(self, args=[]):
            super().__init__("spaCy Text Similarity", args)

    def print_model_info(self):
        pass

    def similarity(self, s1:str, s2:str) -> float: 
        """Compute similarity of 2 sentences"""
        with begin("Computing similarity using spaCy") as op:
            doc1 = nlp(s1)
            doc2 = nlp(s2)
            s = doc1.similarity(doc2)
            op.complete()
            return s