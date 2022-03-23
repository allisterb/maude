import threading
from datetime import timedelta
from time import time
from logging import info, error, debug, warning
from queue import Queue

import click
from multibase import encode as multi_encode

import maude_global
import text.perspective_classifier
from core import ipfs, server
from cli.commands import server as servercmd
from cli.ipfs_commands import init_ipfs_client
from cli.util import exit_with_error

@servercmd.command()  
@click.option('--ipfs-node')
@click.option('--id', default='maude')
@click.argument('perspective_api_key', envvar='PERSPECTIVE_API_KEY', default=None)
def subscribe(ipfs_node, id, perspective_api_key):
    init_ipfs_client(ipfs_node)
    subtopic = id + '_to' 
    pubtopic = id 
    info(f'Maude instance id is {id}.')
    info(f'Subscribed to IPFS topic {subtopic}.')
    info(f'Publishing to IPFS topic {pubtopic}.')
    if not perspective_api_key is None:
        text.perspective_classifier.api_key = perspective_api_key
        server.perspective_classifier = text.perspective_classifier.TextClassifier()
        info(f'Google Perspective API key is {perspective_api_key[0:2]}...')
    else:
        info('No Google Perspective API key found.')
    
    message_queue = Queue()
    encoded_subtopic = str(multi_encode('base64url', subtopic), 'utf-8')
    message_queue = Queue()
    message_count = 0
    start_time = time()
    message_queue_thread = threading.Thread(target=ipfs.subscribe, args=(encoded_subtopic, message_queue), name='message_queue_thread', daemon=True)
    message_queue_thread.start()
    ipfs_subscribe_timeout = False
    stop_monitoring_queue = False
    last_log_message = ''

    while ((not maude_global.KBINPUT) and (not stop_monitoring_queue)):
        while not message_queue.empty():
            message = message_queue.get()
            debug(f'Message received for topic {subtopic}: {message}')
            if message == 'stop':
                stop_monitoring_queue = True
            elif message == 'timeout':
                ipfs_subscribe_timeout = True
            else:
                message_count += 1
                server.process_sub_message(message, pubtopic)
        
        if not message_queue_thread.is_alive():
            if not(ipfs_subscribe_timeout):
                exit_with_error(f'An error occurred monitoring the message queue for topic {subtopic}.')
            else:
                debug('Restarting IPFS subscription after timeout.')
                message_queue_thread = threading.Thread(target=ipfs.subscribe, args=(f, message_queue), name='message_queue_thread', daemon=True)
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
@click.option('--id', default='maude')
@click.argument('log-file', type=click.Path(exists=True), default='ipfs.log')
def monitor(ipfs_node, id, log_file):
    init_ipfs_client(ipfs_node)
    pubtopic = id
    info(f'IPFS log file is {log_file}.')
    info(f'Publishing to IPFS topic {pubtopic}.')
    
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
                if server.process_log_entry(message, pubtopic):
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