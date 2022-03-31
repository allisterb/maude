# Contains code from https://github.com/airbnb/binaryalert/blob/master/rules/compile_rules.py

import os
from logging import info, error
from typing import Generator

import yara

import maude_global
from base.timer import begin
from core.binary_classifier import BinaryClassifier

def _find_yara_files(rules_dir) -> Generator[str, None, None]:
    """Find all .yar[a] files in the rules directory.

    Yields:
        YARA rule filepaths, relative to the rules root directory.
    """
    for root, _, files in os.walk(rules_dir):
        for filename in files:
            lower_filename = filename.lower()
            if lower_filename.endswith('.yar') or lower_filename.endswith('.yara'):
                yield os.path.relpath(os.path.join(root, filename), start=rules_dir)


def compile_rules(rules_dir, target_path: str) -> None:
    """Compile YARA rules into a single binary rules file.

    Args:
        target_path: Where to save the compiled rules file.
    """
    # Each rule file must be keyed by an identifying "namespace"; in our case the relative path.
    yara_filepaths = {relative_path: os.path.join(rules_dir, relative_path)
                    for relative_path in _find_yara_files(rules_dir)}

    # Compile all available YARA rules. Note that external variables are defined but not set;
    # these will be set at runtime by the lambda function during rule matching.
    rules = yara.compile(
        filepaths=yara_filepaths,
        externals={'extension': '', 'filename': '', 'filepath': '', 'filetype': ''})
    rules.save(target_path)

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