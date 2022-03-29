import os
from logging import info

import tensorflow as tf
import onnxruntime

import maude_global
from base.timer import begin
from core.video_classifier import VideoClassifier
from NudeNet.nudenet import NudeClassifier, NudeDetector

class Classifier(VideoClassifier):
    """NudeNet machine learning model"""

    def __init__(self):
        super().__init__("NudeNet machine learning model", os.path.join(maude_global.MAUDE_DIR, 'models', 'nudenet'))
        with begin(f'Loading video classification model: {self.model_dir}') as op:
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

    def classify(self, video_source):
        return self.classifier.classify_video(video_source)

    def detect_objects(self, video_source):
        return self.detector.detect_video(video_source)