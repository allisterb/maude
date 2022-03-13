import os, sys

import spacy
from timer import begin

from logging import info, error, warn, debug
from text_similarity import TextSimilarity

class TextSimilarity(TextSimilarity):
    def __init__(self, args=[]):
            super().__init__("spaCy Text Similarity", args)
            with begin('Loading spaCy model en_core_web_lg') as op:
                self.nlp = spacy.load("en_core_web_lg")
                op.complete()

    def print_model_info(self):
        pass

    def similarity(self, s1:str, s2:str)->float: 
        """Compute similarity of 2 sentences"""
        with begin("Computing similarity using spaCy") as op:
            doc1 = self.nlp(s1)
            doc2 = self.nlp(s2)
            s = doc1.similarity(doc2)
            op.complete()
            return s