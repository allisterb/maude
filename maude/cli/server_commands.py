import threading

from datetime import timedelta
from time import time, sleep
from logging import info, error, debug
from queue import Queue

import click
from multibase import encode

import maude_global
from core import ipfs, server
from cli.commands import server as servercmd
from cli.ipfs_commands import init_ipfs_client
from cli.util import exit_with_error

@servercmd.command()  
@click.option('--ipfs-node')
@click.argument('forum')
def subscribe(ipfs_node, forum:str):
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
            debug(f'Message received for topic {forum}: {message}')
            if message == 'stop':
                stop_monitoring_queue = True
            elif message == 'timeout':
                ipfs_subscribe_timeout = True
            else:
                message_count += 1
                server.process_forum_message(message)
        if not message_queue_thread.is_alive():
            if not(ipfs_subscribe_timeout):
                exit_with_error(f'An error occurred monitoring the message queue for topic {forum}.')
            else:
                debug('Restarting IPFS subscription after timeout.')
                message_queue_thread = threading.Thread(target=ipfs.get_messages, args=(ipfs.ipfsclient, f, message_queue), name='message_queue_thread', daemon=True)
                message_queue_thread.start()
        running_time = time() - start_time
        if int(running_time) % 60 == 0:
            log_message = f'maude server running in subscribe mode for {timedelta(seconds=int(running_time))}. Processed {message_count} total messages. Press [ENTER] to shutdown.'
            if not log_message == last_log_message: 
                info(f'maude server running in subscribe mode for {timedelta(seconds=int(running_time))}. Processed {message_count} total messages. Press [ENTER] to shutdown.')
                last_log_message = log_message
    
    info("maude server shutdown.")

@servercmd.command()  
@click.option('--ipfs-node')
@click.argument('log-file', type=click.Path(exists=True), default='ipfs.log')
def monitor(ipfs_node, log_file):
    init_ipfs_client(ipfs_node)
    debug(f'Log file is {log_file}.')
    message_queue = Queue()
    message_count = 0
    start_time = time()
    message_queue_thread = threading.Thread(target=ipfs.tail_log_file, args=(open(log_file,"r"), message_queue), name='message_queue_thread', daemon=True)
    message_queue_thread.start()
    stop_monitoring_queue = False
    last_log_message = ''
    while ((not maude_global.KBINPUT) and (not stop_monitoring_queue)):
        while not message_queue.empty():
            message = message_queue.get()
            if message == 'stop':
                stop_monitoring_queue = True
            else:
                debug(f'Log entry read: {message}')
                server.process_log_entry(message)
                message_count += 1
        if not message_queue_thread.is_alive():
             exit_with_error(f'An error occurred reading the IPFS log file {log_file}.')
        running_time = time() - start_time
        if int(running_time) % 60 == 0:
            log_message = f'maude server running in monitor mode for {timedelta(seconds=int(running_time))}. Processed {message_count} total log entries. Press [ENTER] to shutdown.'
            if not log_message == last_log_message: 
                info(f'maude server running in monitor mode for {timedelta(seconds=int(running_time))}. Processed {message_count} total log entries. Press [ENTER] to shutdown.')
                last_log_message = log_message
    
    info("maude server shutdown.")
       
        

    

