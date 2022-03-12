import os
import sys
from logging import info, error, debug, warn

from image_classifier import ImageClassifier

from nsfw_model.nsfw_detector import predict

class Classifier(ImageClassifier):
    """NSFW Detection Machine Learning Model"""

    def __init__(self, image_source, args):
        print('path:' + os.path.abspath('models'))
        super().__init__("NSFW Detection Machine Learning Model", os.path.join('models', 'mobilenet_v2_140_224'), image_source, args)
        self.model_file = os.path.join(self.model_dir, 'saved_model.h5')
        if not os.path.exists(self.model_file):
            error(f'{self.model_file} does not exist.')
            sys.exit(1)

    def print_model_info(self):
        pass

    def get_label_for_index(self, _):
        return ''