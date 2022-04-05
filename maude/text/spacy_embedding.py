import spacy

from base.timer import begin
from core.text_embedding import SentenceEmbedding

class WordAverageEmbedding(SentenceEmbedding):
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
        doc1 = self.nlp(s1)
        doc2 = self.nlp(s2)
        return doc1.similarity(doc2)

class UseEmbedding(SentenceEmbedding):
    def __init__(self, args=[]):
            super().__init__("Google Universal Sentence Encoder sentence encoding", args)
            import spacy_universal_sentence_encoder
            with begin('Loading Google Universal Sentence Encoder model') as op:
                self.nlp = spacy_universal_sentence_encoder.load_model('en_use_lg')
                op.complete()

    def get_model_info(self):
        pass

    def get_vector(self, sentence:str):
        return self.nlp(sentence).vector

    def similarity(self, s1:str, s2:str) -> float: 
        """Compute similarity of 2 sentences"""
        doc1 = self.nlp(s1)
        doc2 = self.nlp(s2)
        return doc1.similarity(doc2)