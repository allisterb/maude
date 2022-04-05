import os

from base.timer import begin
from maude_global import MAUDE_DIR
from core.image_classifier import ImageClassifier
from nsfw_model.nsfw_detector import predict

class Classifier(ImageClassifier):
    """NSFW Detection Machine Learning Model"""

    def __init__(self):
        super().__init__("NSFW Detection Machine Learning Model", os.path.join(MAUDE_DIR, 'models', 'mobilenet_v2_140_224'))
        import tensorflow as tf
        with begin(f'Loading image classification model: {self.model_dir}') as op:
            tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)  # or any {DEBUG, INFO, WARN, ERROR, FATAL}
            self.model = predict.load_model(self.model_dir)
            op.complete()
        
    def get_model_info(self):
        pass

    def get_label_for_index(self, _):
        return ''

    def classify(self, image_source):
        with begin(f'Classifying {image_source} using NudeNet') as op:
            d = predict.classify(self.model, image_source)
            op.complete()
            return list(d.values())[0]
        