import os, sys
import abc
from logging import info, error, warn, debug

from cli_util import *

class DataImporter(abc.ABC):
    """Import topic, comment and image data for training moderation models."""

    def __init__(self, args=[]):
        self.args = args

    @abc.abstractmethod
    def print_importer_info(self):
        """Print out information on model"""
    
    @abc.abstractmethod
    def import_data():
        """Import data using the parameters specified in the DataImporter constructor"""