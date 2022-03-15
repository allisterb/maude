from email import message
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

@server.command('run')  
@click.option('--ipfs-node')
@click.argument('forum')
def run(ipfs_node, forum:str):
    init_ipfs_client(ipfs_node)
    f = str(encode('base64url', "test"), 'utf-8')
    message_queue = Queue()
    message_count = 0
    info(f'Forum id is {f}.')
    start_time = time()
    message_queue_thread = threading.Thread(target=ipfs.get_messages, args=(ipfs.ipfsclient, 'test', message_queue), name='message_queue_thread', daemon=True)
    message_queue_thread.start()
    stop = False
    while ((not maude_global.KBINPUT) and (not stop)):
        if not message_queue_thread.is_alive():
            message_queue_thread = threading.Thread(target=ipfs.get_messages, args=(ipfs.ipfsclient, f, message_queue), name='message_queue_thread', daemon=True)
            message_queue_thread.start()
        while message_queue.not_empty:
            message = message_queue.get()
            print(message)
            message_count += 1
        running_time = time() - start_time
        #if int(running_time) % 5 == 0:
        info(f'maud3 server running for {"{:0.2f}".format(running_time)} s. Processed {message_count} messages this iteration. Press [ENTER] to shutdown.')
        sleep(1)
    info('exit loop')
    with begin("Server shutting down") as op:
        op.complete()
        

    

