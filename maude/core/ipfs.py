import os
import time

from logging import debug,error
import queue

from pyipfs import ipfshttpclient

from base.timer import begin

ipfsclient:ipfshttpclient.Client = None

def get_client_id():
    return ipfsclient.id()

def get_config(key=None):
    config = ipfsclient.config.get()
    if key == None:
        return config
    else:
        try:
            return config[key]
        except KeyError as _:
            error(f'The config key \'{key}\' does not exist.')
            return None
        except Exception as e:
            error(f'An error occurred getting the config key \'{key}\': {e}.')
            return None

def get_pubsub_messages(client:ipfshttpclient.Client, topic:str, q:queue.Queue):
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

def get_log(client:ipfshttpclient.Client, q:queue.Queue):
    debug(f'Subscribing to IPFS log...')
    try:
        with client.log.log_tail() as sub:
            debug(f'Subscribed.')
            for message in sub:
                q.put(message)
    except Exception as e:
        ex_msg = f'Exception subscribing to log: {e}'
        debug(f'Exception subscribing to log: {e}')
        if str(ex_msg).endswith('Read timed out.'):
            q.put('timeout')
        else:
            error(ex_msg)
            q.put('stop')

def tail_log_file(file):
    file.seek(0, os.SEEK_END)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line
