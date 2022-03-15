import json
import threading

from datetime import timedelta
from time import time, sleep
from logging import info, error, debug
from queue import Queue

import click
from multibase import encode

import maude_global
from base.timer import begin
from core import ipfs, server
from cli.commands import server as servergroup
from cli.ipfs_commands import init_ipfs_client
from cli.util import exit_with_error

@servergroup.command('run')  
@click.option('--ipfs-node')
@click.argument('forum')
def run(ipfs_node, forum:str):
    init_ipfs_client(ipfs_node)
    f = str(encode('base64url', forum), 'utf-8')
    message_queue = Queue()
    message_count = 0
    debug(f'Forum topic is {f}.')
    start_time = time()
    message_queue_thread = threading.Thread(target=ipfs.get_messages, args=(ipfs.ipfsclient, f, message_queue), name='message_queue_thread', daemon=True)
    message_queue_thread.start()
    ipfs_subscribe_timeout = False
    stop_monitoring_queue = False
    while ((not maude_global.KBINPUT) and (not stop_monitoring_queue)):
        while not message_queue.empty():
            message = message_queue.get()
            debug(f'Message received for topic test: {message}')
            message_count += 1
            if message == 'stop':
                stop_monitoring_queue = True
            elif message == 'timeout':
                ipfs_subscribe_timeout = True
            else:
                server.process_forum_message(message)
        if not message_queue_thread.is_alive():
            if not(maude_global.KBINPUT or ipfs_subscribe_timeout):
                exit_with_error(f'An error occurred monitoring the message queue for forum {forum}.')
            elif ipfs_subscribe_timeout:
                debug('Restarting IPFS subscription after timeout.')
                message_queue_thread = threading.Thread(target=ipfs.get_messages, args=(ipfs.ipfsclient, f, message_queue), name='message_queue_thread', daemon=True)
                message_queue_thread.start()
            else:
                break
        running_time = time() - start_time
        if int(running_time) % 5 == 0:
            info(f'maud3 server running for {timedelta(seconds=int(running_time))}. Processed {message_count} message(s) for forum {forum}. Press [ENTER] to shutdown.')
        sleep(1)
        
    info("maud3 server shutdown.")
       
        

    

