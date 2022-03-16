import queue
import subprocess
from logging import debug,error

from pyipfs import ipfshttpclient

from base.timer import begin

ipfsclient:ipfshttpclient.Client = None

def get_client_id():
    return ipfsclient.id()

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

# def monitor_node_log(client:ipfshttpclient.Client):
#    debug(f'Running ipfs tail log command...')
#    p = subprocess.Popen('ipfs tail lo', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
#    stdout = []
#    while True:
#        line = p.stdout.readline()
#        stdout.append(line)
#       print(line),
#        if p.poll() != None:
#            break
#    return ''.join(stdout)