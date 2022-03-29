import abc
from logging import info

from PIL import Image

class ImageClassifier(abc.ABC):
    """An image classifier using a neural network or other computer vision classification model"""

    @abc.abstractmethod
    def get_label_for_index(self, i):
        """Get the string label for an integer index"""

    @abc.abstractmethod
    def get_model_info(self):
        """Get information on model used for classification"""

    @abc.abstractmethod
    def classify(self, image_source):
        """Classify the specified image"""
        
    def __init__(self, name, model_dir='', args={}):
        self.name = name
        self.model_dir = model_dir
        self.args = args

    def get_image(self, image_source):
        image = Image.open(image_source)
        info('Image: %sw x %sh %s', image.width, image.height, image.format)
        return image