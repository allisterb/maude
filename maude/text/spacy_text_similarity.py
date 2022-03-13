import os, sys
import abc
from logging import info, error, warn, debug
from text_similarity import TextSimilarity

class SpacyTextSimilarity(TextSimilarity):
        def __init__(self, args=[]):
                super().__init__("spaCy Text Similarity", args)
                