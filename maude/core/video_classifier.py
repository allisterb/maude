import abc
from logging import info

class VideoClassifier(abc.ABC):
    """A video classifier using a neural network or other computer vision classification model"""

    @abc.abstractmethod
    def get_label_for_index(self, i):
        """Get the string label for an integer index"""

    @abc.abstractmethod
    def get_model_info(self):
        """Get information on model used for classification"""

    @abc.abstractmethod
    def classify(self, video_source):
        """Classify the specified video"""
        
    def __init__(self, name, model_dir='', args={}):
        self.name = name
        self.model_dir = model_dir
        self.args = args