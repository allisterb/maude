import os
from logging import info

import tensorflow as tf
import onnxruntime

import maude_global
from base.timer import begin
from core.image_classifier import ImageClassifier
from NudeNet.nudenet import NudeClassifier

class Classifier(ImageClassifier):
    """NudeNet Detection Machine Learning Model"""

    def __init__(self):
        super().__init__("NudeNet Machine Learning Model", os.path.join(maude_global.MAUDE_DIR, 'models', 'nudenet'))
        with begin(f'Loading model: {self.model_dir}') as op:
            if not maude_global.DEBUG:
                tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)  # or any {DEBUG, INFO, WARN, ERROR, FATAL}
                onnxruntime.set_default_logger_severity(3)
            self.classifier = NudeClassifier(self.model_dir)
            op.complete()
        
    def get_model_info(self):
        pass

    def get_label_for_index(self, _):
        return ''

    def classify(self, image_source):
        return self.classifier.classify(image_source)