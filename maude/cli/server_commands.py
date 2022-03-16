import json
import threading

from datetime import timedelta
from time import time, sleep
from logging import info, error, debug
from queue import Queue

import click
from multibase import encode
from rich import print
import maude_global
from base.timer import begin
from core import ipfs, server
from cli.commands import server as servercmd
from cli.ipfs_commands import init_ipfs_client
from cli.util import exit_with_error

@servercmd.command('run')  
@click.option('--ipfs-node')
@click.argument('forum')
def run(ipfs_node, forum:str):
    init_ipfs_client(ipfs_node)
    f = str(encode('base64url', forum), 'utf-8')
    message_queue = Queue()
    message_count = 0
    debug(f'Forum topic is {f}.')
    start_time = time()
    message_queue_thread = threading.Thread(target=ipfs.get_pubsub_messages, args=(ipfs.ipfsclient, f, message_queue), name='message_queue_thread', daemon=True)
    message_queue_thread.start()
    ipfs_subscribe_timeout = False
    stop_monitoring_queue = False
    last_log_message = ''
    while ((not maude_global.KBINPUT) and (not stop_monitoring_queue)):
        while not message_queue.empty():
            message = message_queue.get()
            debug(f'Message received for topic test: {message}')
            if message == 'stop':
                stop_monitoring_queue = True
            elif message == 'timeout':
                ipfs_subscribe_timeout = True
            else:
                message_count += 1
                server.process_forum_message(message)
        if not message_queue_thread.is_alive():
            if not(ipfs_subscribe_timeout):
                exit_with_error(f'An error occurred monitoring the message queue for forum {forum}.')
            else:
                debug('Restarting IPFS subscription after timeout.')
                message_queue_thread = threading.Thread(target=ipfs.get_messages, args=(ipfs.ipfsclient, f, message_queue), name='message_queue_thread', daemon=True)
                message_queue_thread.start()
        running_time = time() - start_time
        if int(running_time) % 5 == 0:
            log_message = f'maud3 server running for {timedelta(seconds=int(running_time))}. Processed {message_count} message(s). Press [ENTER] to shutdown.'
            if not log_message == last_log_message: 
                info(f'maud3 server running for {timedelta(seconds=int(running_time))}. Processed {message_count} message(s). Press [ENTER] to shutdown.')
                last_log_message = log_message
    
    info("maud3 server shutdown.")

@servercmd.command('monitor')  
@click.option('--ipfs-node')
def monitor(ipfs_node):
    init_ipfs_client(ipfs_node)
    message_queue = Queue()
    message_count = 0
    start_time = time()
    message_queue_thread = threading.Thread(target=ipfs.get_log, args=(ipfs.ipfsclient, message_queue), name='message_queue_thread', daemon=True)
    message_queue_thread.start()
    ipfs_subscribe_timeout = False
    stop_monitoring_queue = False
    last_log_message = ''
    while ((not maude_global.KBINPUT) and (not stop_monitoring_queue)):
        while not message_queue.empty():
            message = message_queue.get()
            if message['system'] == 'addrutil':
                continue
            debug(f'Log message received: {message}')
            if message == 'stop':
                stop_monitoring_queue = True
            elif message == 'timeout':
                ipfs_subscribe_timeout = True
            else:
                message_count += 1
        if not message_queue_thread.is_alive():
            if not(ipfs_subscribe_timeout):
                exit_with_error(f'An error occurred monitoring the message queue for.')
            else:
                debug('Restarting IPFS subscription after timeout.')
                message_queue_thread = threading.Thread(target=ipfs.get_log, args=(ipfs.ipfsclient, message_queue), name='message_queue_thread', daemon=True)
                message_queue_thread.start()
        running_time = time() - start_time
        if int(running_time) % 5 == 0:
            log_message = f'maud3 server running for {timedelta(seconds=int(running_time))}. Processed {message_count} message(s). Press [ENTER] to shutdown.'
            if not log_message == last_log_message: 
                info(f'maud3 server running for {timedelta(seconds=int(running_time))}. Processed {message_count} message(s). Press [ENTER] to shutdown.')
                last_log_message = log_message
    
    info("maud3 server shutdown.")
       
        

    

