import abc
from logging import info

class BinaryClassifier(abc.ABC):
    """Scan and classify a binary executable or archive using a malware detector or other classifier"""

    @abc.abstractmethod
    def get_info(self):
        """Get information on binary classifier"""

    @abc.abstractmethod
    def classify(self, filename):
        """Classify the specified binary"""
        
    def __init__(self, name, model_dir='', args={}):
        self.name = name
        self.model_dir = model_dir
        self.args = args