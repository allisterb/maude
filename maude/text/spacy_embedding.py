from logging import info, error, warn, debug

import spacy

from base.timer import begin
from core.text_embedding import SentenceEmbedding

class Embedding(SentenceEmbedding):
    def __init__(self, args=[]):
            super().__init__("spaCy sentence embedding using averaged word-vectors", args)
            with begin('Loading spaCy model en_core_web_lg') as op:
                self.nlp = spacy.load("en_core_web_lg")
                op.complete()

    def get_model_info(self):
        pass

    def get_vector(self, sentence:str):
        return self.nlp(sentence).vector

    def similarity(self, s1:str, s2:str) -> float: 
        """Compute similarity of 2 sentences"""
        with begin("Computing similarity using spaCy sentence embedding using averaged word vectors") as op:
            doc1 = self.nlp(s1)
            doc2 = self.nlp(s2)
            s = doc1.similarity(doc2)
            op.complete()
            return s