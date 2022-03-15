import queue
from logging import debug,error

from pyipfs import ipfshttpclient

from base.timer import begin

ipfsclient:ipfshttpclient.Client = None

def get_client_id():
    return ipfsclient.id()

def get_messages(client:ipfshttpclient.Client, topic:str, q:queue.Queue):
    debug(f'Subscribing to topic {topic}...')
    try:
        with client.pubsub.subscribe(topic) as sub:
            for message in sub:
                q.put(message)
    except Exception as e:
        error(f'An error occurred subscribing to {topic}: {e}.')
        q.put('stop')
        



