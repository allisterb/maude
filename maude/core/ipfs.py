import queue
from logging import debug,error

from pyipfs import ipfshttpclient

from base.timer import begin

ipfsclient:ipfshttpclient.Client = None

def get_client_id():
    return ipfsclient.id()

def get_messages(client:ipfshttpclient.Client, topic:str, q:queue.Queue):
    debug(f'Subscribing to IPFS topic {topic}...')
    try:
        with client.pubsub.subscribe(topic) as sub:
            debug(f'Subscribed.')
            for message in sub:
                q.put(message)
    except Exception as e:
        ex_msg = f'Exception subscribing to {topic}: {e}'
        debug(f'Exception subscribing to {topic}: {e}')
        if str(ex_msg).endswith('Read timed out.'):
            q.put('timeout')
        else:
            error(ex_msg)
            q.put('stop')