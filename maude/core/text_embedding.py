import os, sys
import abc
from logging import info, error, warn, debug

class SentenceEmbedding(abc.ABC):
    """Represent sentences as vectors"""

    def __init__(self, name, args=[]):
        self.name = name
        self.args = args

    @abc.abstractmethod
    def print_model_info(self)->None:
        """Print out information on model"""

    @abc.abstractmethod
    def similarity(s1:str, s2:str)->float: 
        """Compute similarity of 2 sentences"""
