import os

import tensorflow as tf

from logging import info, error, debug, warn
from maude_global import MAUDE_DIR
from core.image_classifier import ImageClassifier
from nsfw_model.nsfw_detector import predict

class Classifier(ImageClassifier):
    """NSFW Detection Machine Learning Model"""

    def __init__(self, image_source, args={}):
        super().__init__("NSFW Detection Machine Learning Model", os.path.join(MAUDE_DIR, 'models', 'mobilenet_v2_140_224'), image_source, args)
        tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)  # or any {DEBUG, INFO, WARN, ERROR, FATAL}
        self.model = predict.load_model(self.model_dir)
        info('Model: %s', self.model_dir)
        
    def print_model_info(self):
        pass

    def get_label_for_index(self, _):
        return ''

    def classify(self):
        return predict.classify(self.model, self.image_source)