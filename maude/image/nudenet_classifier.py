import os
from logging import info

import tensorflow as tf

from base.timer import begin
from maude_global import MAUDE_DIR
from core.image_classifier import ImageClassifier
from NudeNet.nudenet import NudeClassifier

class Classifier(ImageClassifier):
    """NudeNet Detection Machine Learning Model"""

    def __init__(self):
        super().__init__("NudeNet Machine Learning Model", os.path.join(MAUDE_DIR, 'models', 'nudenet'))
        with begin(f'Loading model: {self.model_dir}') as op:
            tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)  # or any {DEBUG, INFO, WARN, ERROR, FATAL}
            self.classifier = NudeClassifier(self.model_dir)
            op.complete()
        
    def get_model_info(self):
        pass

    def get_label_for_index(self, _):
        return ''

    def classify(self, image_source):
        return self.classifier.classify(image_source)