import os
import sys
import tensorflow as tf

from logging import info, error, debug, warn
from maude_global import MAUDE_DIR, DEBUG

if DEBUG:
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}  to control TensorFlow 2 logging level
    tf.get_logger().setLevel('DEBUG')
else:
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'  # or any {'0', '1', '2'}  to control TensorFlow 2 logging level
    tf.get_logger().setLevel('INFO')
   
from image_classifier import ImageClassifier
from nsfw_model.nsfw_detector import predict

class Classifier(ImageClassifier):
    """NSFW Detection Machine Learning Model"""

    def __init__(self, image_source, args):
        super().__init__("NSFW Detection Machine Learning Model", os.path.join(MAUDE_DIR, 'models', 'mobilenet_v2_140_224'), image_source, args)
        self.model_file = os.path.join(self.model_dir, 'saved_model.h5')
        if not os.path.exists(self.model_file):
            error(f'{self.model_file} does not exist.')
            sys.exit(1)
        else:
            info(f'Using model file: {os.path.abspath(self.model_file)}')

    def print_model_info(self):
        pass

    def get_label_for_index(self, _):
        return ''