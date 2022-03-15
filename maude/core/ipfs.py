from distutils import core
from pyipfs import ipfshttpclient

ipfsclient:ipfshttpclient.Client = None

def get_client_id():
    return ipfsclient.id()
