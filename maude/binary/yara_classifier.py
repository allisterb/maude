import os
from logging import info, error

import yara

import maude_global
from base.timer import begin
from core.binary_classifier import BinaryClassifier

class Classifier(BinaryClassifier):
    """YARA binary classiifier"""

    def __init__(self):
        super().__init__("YARA binary classiifier", os.path.join(maude_global.MAUDE_DIR, 'models', 'yara'))
        with begin(f'Loading YARA rules: {self.model_dir}') as op:
            self.rules = yara.load(filepath=self.model_dir)
            op.complete()
        
    def classify(self, filename):
        with begin(f'Classifying {filename} using NudeNet') as op:
            matches = self.rules.match(filename)
            op.complete()
            return matches 
        