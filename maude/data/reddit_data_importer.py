import os, sys
import abc
from logging import info, error, warn, debug

from core.data_importer import DataImporter

class DataImporter(DataImporter):
    """Import topic, comment and image data from Reddit."""

    def __init__(self, client_id, client_secret, client_user, client_pass, args=[]):
        self.client_id=client_id
        self.client_secret=client_secret
        self.client_user = client_user
        self.client_pass=client_pass
        self.args = args
        info(f'Client id is {self.client_id}. Client user is {self.client_user}.')

    def get_importer_info(self):
        """Print out information on model"""
        pass
    
    def import_data(self, *args):
        """Import data using the parameters specified in the DataImport constructor"""
        print(args)



    