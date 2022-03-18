import os, sys
import abc
from logging import info, error, warn, debug

class TextClassifier(abc.ABC):
    """An text classifier using a neural network or other NLU classification model"""

    @abc.abstractmethod
    def print_model_info(self):
        """Print out information on model"""

    @abc.abstractmethod
    def classify():
        """Classify the specified text"""

    def __init__(self, name, args):
        self.name = name
        self.args = args
