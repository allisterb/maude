from http import client
from pyipfs import ipfshttpclient

client = ipfshttpclient.connect(session=True)

def get_client_id():
    return client.id()