import os
from logging import info

import PIL


import maude_global
from base.timer import begin
from core.image_classifier import ImageClassifier
from NudeNet.nudenet import NudeClassifier, NudeDetector

class Classifier(ImageClassifier):
    """NudeNet detection machine learning model"""

    def __init__(self):
        super().__init__("NudeNet machine learning model", os.path.join(maude_global.MAUDE_DIR, 'models', 'nudenet'))
        import tensorflow as tf
        import onnxruntime
        with begin(f'Loading image classification model: {self.model_dir}') as op:
            if not maude_global.DEBUG:
                tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)  # or any {DEBUG, INFO, WARN, ERROR, FATAL}
                onnxruntime.set_default_logger_severity(3)
            #else:
                #tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.DEBUG)  # or any {DEBUG, INFO, WARN, ERROR, FATAL}
                #onnxruntime.set_default_logger_severity(1)
            self.classifier = NudeClassifier(self.model_dir)
            self.detector = NudeDetector(self.model_dir)
            op.complete()
        
    def get_model_info(self):
        pass

    def get_label_for_index(self, _):
        return ''

    def classify(self, image_source):
        with begin(f'Classifying {image_source} using NudeNet') as op:
            image = self.get_image(image_source)
            cd = self.classifier.classify(image_source)
            dd = self.detector.detect(image_source)
            data = list(cd.values())[0] 
            data['height'] = image.height
            data['width'] = image.width
            data['format'] = image.format
            image.close()
            data['objects'] = dd
            op.complete()
            return data 
        