import os
import time
import queue
from logging import info, debug, error

from pyipfs import ipfshttpclient

import maude_global
from base.timer import begin

ipfsclient:ipfshttpclient.Client = None

object_links_cache = dict()
object_cache = dict()
dag_node_cache = dict()

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

def subscribe(topic:str, q:queue.Queue):
    debug(f'Subscribing to IPFS topic {topic}...')
    try:
        with ipfsclient.pubsub.subscribe(topic) as sub:
            debug(f'Subscribed.')
            for message in sub:
                q.put(message)
    except Exception as e:
        ex_msg = f'Exception subscribing to {topic}: {e}'
        debug(ex_msg)
        if str(ex_msg).endswith('Read timed out.'):
            q.put('timeout')
        else:
            error(ex_msg)
            q.put('stop')

def publish(topic:str, msg:str):
    with begin(f'Publishing message with length {len(msg)} to IPFS topic {topic}') as op:
        ipfsclient.pubsub.publish(topic, msg)
        op.complete()

def tail_log_file(file, q:queue.Queue):
    file.seek(0, os.SEEK_END)
    while not maude_global.KBINPUT:
        line = file.readline()
        if not line:
            time.sleep(1)
            continue
        #yield line
        q.put(line)

def tail_event_log(q:queue.Queue):
    debug("Connecting to event log...")
    try:
        with ipfsclient.log.log_tail() as sub:
            debug("Connected.")
            for message in sub:
                q.put(message)
    except Exception as e:
        ex_msg = f'Exception reading event log: {e}'
        debug(f'Exception reading event log: {e}')
        if str(ex_msg).endswith('Read timed out.'):
            q.put('timeout')
        else:
            error(ex_msg)
            q.put('stop')

def get_file(file_hash:str):
    with begin(f'Retrieving file {file_hash}') as op:
        f = ipfsclient.cat(file_hash)
        op.complete()
        return f

def get_object(cid:str):
    if not cid in object_cache:
        debug(f'Requesting object with cid {cid}.')
        object_cache[cid] = ipfsclient.object.get(cid)
    return object_cache[cid]
    
def get_dag_node(cid:str):
    if not cid in dag_node_cache:
        debug(f'Requesting DAG node with cid {cid}.')
        dag_node_cache[cid] = ipfsclient.dag.get(cid)
    return dag_node_cache[cid]

def get_links(cid:str):
    if not cid in object_links_cache:
        debug(f'Requesting links for cid {cid}.')
        object_links_cache[cid] = ipfsclient.object.links(cid)
    return object_links_cache[cid]

def is_file_or_dir(cid:str):
    if 'Links' in get_links(cid):
        return True
    else:
        #return not (len(object_links_cache[cid]) == 1 and 'Hash' in object_links_cache[cid] and object_links_cache[cid]['Hash'] == cid)
        return False