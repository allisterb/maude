import threading
from time import time, sleep
from logging import info, error, debug
from queue import Queue

import click
from rich import print
from pyipfs import ipfshttpclient
from multibase import encode

import maude_global
from base.timer import begin
from core import ipfs
from cli.commands import server
from cli.ipfs_commands import init_ipfs_client
from cli.util import exit_with_error

@server.command('run')  
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
    stop_monitoring_queue = False
    while ((not maude_global.KBINPUT) and (not stop_monitoring_queue)):
        if not message_queue_thread.is_alive():
            exit_with_error('An error occurred starting the message queue thread.')
        
        while not message_queue.empty():
            message = message_queue.get()
            debug(f'Message received for topic test: {message}')
            message_count += 1
            if message == 'stop':
                stop_monitoring_queue = True
        running_time = time() - start_time
        if int(running_time) % 5 == 0:
            info(f'maud3 server running for {"{:0.2f}".format(running_time)} s. Processed {message_count} message(s) for forum {forum}. Press [ENTER] to shutdown.')
        sleep(1)
        
        if (not message_queue_thread.is_alive()) and (not stop_monitoring_queue):
            message_queue_thread = threading.Thread(target=ipfs.get_messages, args=(ipfs.ipfsclient, f, message_queue), name='message_queue_thread', daemon=True)
            message_queue_thread.start()
    info("maud3 server shutdown.")
       
        

    

