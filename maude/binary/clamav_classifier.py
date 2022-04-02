# Contains code from https://github.com/clamwin/python-clamav/blob/master/clamav.py

import os
import tempfile
from base64 import decode
from ctypes import cdll
from ctypes.util import find_library
from logging import info, error

import maude_global
import binary.clamav as clamav
from base.timer import begin
from core.binary_classifier import BinaryClassifier

def libraryAvailable():
    library = find_library('clamav') or find_library('libclamav') or 'libclamav'
    try:
        _ = cdll[library]
        return True
    except OSError as e:
        return False

class Classifier(BinaryClassifier):
    """ClamAV binary classifier"""

    def __init__(self, tempdir= None):
        super().__init__("ClamAV binary classifier", os.path.join(maude_global.MAUDE_DIR, 'models', 'clamavdb'))
        self.dbpath = os.path.join(maude_global.MAUDE_DIR, 'models', 'clamavdb')
        with begin(f'Loading ClamAV database: {self.dbpath}') as op:
            self.scanner = clamav.Scanner(dbpath=self.dbpath, autoreload=True)
            self.scanner.setEngineOption(clamav.CL_ENGINE_TMPDIR, tempdir if tempdir is not None else tempfile.gettempdir())
            op.complete()
    
    def get_info(self):
        return self.scanner.getVersions()
        
    def classify(self, filename):
        with begin(f'Classifying {filename} using ClamAV database from {self.dbpath}') as op:
            id, sig = self.scanner.scanFile(filename)
            op.complete()
            return id, sig.decode('utf-8')