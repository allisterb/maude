import os, sys

from text.spacy import nlp
from base.timer import begin

from logging import info, error, warn, debug
from core.text_embedding import SentenceEmbedding

class Embedding(SentenceEmbedding):
    def __init__(self, args=[]):
            super().__init__("spaCy sentence embedding", args)

    def get_model_info(self):
        pass

    def get_vector(self, sentence:str):
        return nlp(sentence).vector

    def similarity(self, s1:str, s2:str) -> float: 
        """Compute similarity of 2 sentences"""
        with begin("Computing similarity using spaCy sentence embedding") as op:
            doc1 = nlp(s1)
            doc2 = nlp(s2)
            s = doc1.similarity(doc2)
            op.complete()
            return s