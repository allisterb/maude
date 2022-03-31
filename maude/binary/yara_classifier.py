# Contains code from https://github.com/airbnb/binaryalert/blob/master/rules/compile_rules.py

import collections
import os
from logging import info, error
from typing import Generator
from typing import Any, Dict, List

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

YaraMatch = collections.namedtuple(
    'YaraMatch',
    [
        'rule_name',        # str: Name of the YARA rule
        'rule_namespace',   # str: Namespace of YARA rule (original YARA filename)
        'rule_metadata',    # Dict: String metadata associated with the YARA rule
        'matched_strings',  # Set: Set of string string names matched (e.g. "{$a, $b}")
        'matched_data'      # Set: Matched YARA data
    ]
)

class Classifier(BinaryClassifier):
    """YARA binary classiifier"""

    def __init__(self, ruleset):
        super().__init__("YARA binary classiifier", os.path.join(maude_global.MAUDE_DIR, 'models', 'yara'))
        self.ruleset = ruleset
        self.compiled_rules_file = os.path.join(self.model_dir, self.ruleset + '.yarac')
        with begin(f'Loading YARA rules from compiled rules file: {self.compiled_rules_file}') as op:
            self.rules = yara.load(filepath=self.compiled_rules_file)
            op.complete()
    
    def get_info(self):
        return ''
        
    def classify(self, filename):
        with begin(f'Classifying {filename} using YARA ruleset {self.ruleset}') as op:
            raw_yara_matches = self.rules.match(filename, externals=Classifier._yara_variables(filename)) if self.ruleset == 'binaryalert' else self.rules.match(filename)
            yara_python_matches = []
            for match in raw_yara_matches:
                string_names = set()
                string_data = set()
                for _, name, data in match.strings:
                    string_names.add(name)
                    try:
                        string_data.add(data.decode('utf-8'))
                    except UnicodeDecodeError:
                        # Bytes string is not unicode - print its hex values instead
                        string_data.add(data.hex())
                yara_python_matches.append(
                    YaraMatch(match.rule, match.namespace, match.meta, list(string_names), list(string_data)))
            op.complete()
            return yara_python_matches

    @staticmethod
    def _yara_variables(original_target_path: str) -> Dict[str, str]:
        """Compute external variables needed for some YARA rules.
        Args:
            original_target_path: Path where the binary was originally discovered.
        Returns:
            A map from YARA variable names to their computed values.
        """
        file_name = os.path.basename(original_target_path)
        file_suffix = file_name.split('.')[-1] if '.' in file_name else ''  # e.g. "exe" or "rar".
        return {
            'extension': '.' + file_suffix if file_suffix else '',
            'filename': file_name,
            'filepath': original_target_path,
            'filetype': file_suffix.upper()  # Used in only one rule (checking for "GIF").
        }