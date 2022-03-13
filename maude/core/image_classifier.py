import os, sys
import abc
from logging import info, error, warn, debug
from PIL import Image

from cli.util import *

class ImageClassifier(abc.ABC):
    """An image classifier using a neural network or other computer vision classification model."""

    @abc.abstractmethod
    def get_label_for_index(self, i):
        """Get the string label for an integer index"""

    @abc.abstractmethod
    def print_model_info(self):
        """Print out information on model"""

    @abc.abstractmethod
    def classify():
        """Classify the specified image"""

    def __init__(self, name, model_dir, image_source, args):
        self.name = name
        self.model_dir = model_dir
        self.image_source = exit_if_file_not_exists(image_source)
        self.image = Image.open(image_source)
        self._height, self._width, self._info = self.image.height, self.image.width, self.image.info
        info('Image: %s %sw x %sh %s', self.image_source, self._width, self._height, self.image.format)
        self.args = args
