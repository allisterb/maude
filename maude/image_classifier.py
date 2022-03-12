import sys
import abc
import math
import time
from queue import Queue
from logging import info, error, warn, debug
import kbinput
from PIL import Image

class ImageClassifier(abc.ABC):
    """An image classifier using a neural network or other computer vision classification model."""

    @abc.abstractmethod
    def get_label_for_index(self, i):
        """Get the string label for an integer index."""

    @abc.abstractmethod
    def print_model_info(self):
        """Print out information on model."""

    def __init__(self, name, model_dir, image_source, args):
        self.name = name
        self.model_dir = model_dir
        self.image_source = image_source
        self.image = Image.open(image_source)
        self._height, self._width, self._info = self.image.height, self.image.width, self.image.info
        info(f'Image dimensions: {self._width}x{self._height}')
        self.args = args
