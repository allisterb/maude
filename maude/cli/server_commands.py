import os
import threading
from datetime import timedelta
from time import time
from logging import info, error, debug, warning
from queue import Queue

import click
from rich import print
from multibase import encode as multi_encode
from base.timer import begin

from core import ipfs, server, crypto
import maude_global
import binary.yara_classifier
import binary.clamav_classifier
import text.perspective_classifier
import image.nfsw_classifier
import image.nudenet_classifier
import video.nudenet_classifier
import image.ms_photodna
from cli.commands import server as servercmd
from cli.ipfs_commands import init_ipfs_client
from cli.util import exit_with_error

@servercmd.command(help='Subscribe to an IPFS pubsub topic and listen for requests.')  
@click.option('--id', default='maude', help='The maude instance id.')
@click.option('--ipfs-node', default='/dns/localhost/tcp/5001/http', help='The address of the IPFS node API to connect to.')
@click.option('--keyfile', default='[id].pem', help='The private-key file to use.')
@click.argument('perspective_api_key', envvar='PERSPECTIVE_API_KEY', default=None)
def subscribe(id, ipfs_node, keyfile, perspective_api_key):
    maude_global.MAUDE_ID = id
    init_ipfs_client(ipfs_node)
    if keyfile == '[id].pem':
        keyfile = id + '.pem'
    if not os.path.exists(keyfile):
        exit_with_error(f'The private key file {keyfile} does not exist. Run `maude crypto gen` to generate a public/private-key pair.')
    with begin(f'Loading private key from {keyfile}') as op:
        crypto.load_private_key(keyfile)
        op.complete()
    subtopic = id + '_to' 
    pubtopic = id 
    info(f'Maude instance id is {id}.')
    info(f'Subscribed to IPFS topic {subtopic} for moderation requests.')
    info(f'Publishing moderation data to IPFS topic {pubtopic}.')
    
    with begin('Loading classifiers') as op:
        if not perspective_api_key is None:
            text.perspective_classifier.api_key = perspective_api_key
            server.perspective_classifier = text.perspective_classifier.TextClassifier()
            info(f'Google Perspective API key is {perspective_api_key[0:2]}...')
        else:
            info('No Google Perspective API key found.')
        server.yara_classifier = binary.yara_classifier.Classifier('binaryalert')
        server.clamAVAvailable = binary.clamav_classifier.libraryAvailable()
        if server.clamAVAvailable:
            server.clamav_classifier = binary.clamav_classifier.Classifier()
        else:
            error('ClamAV not available. Check that libclamav libraries are installed.')
        server.nsfw_classifier = image.nfsw_classifier.Classifier()
        server.nudenet_image_classifier = image.nudenet_classifier.Classifier()
        server.nudenet_video_classifier = video.nudenet_classifier.Classifier()
        server.photoDNAHashAvailable = image.ms_photodna.libraryAvailable()
        op.complete()

    message_queue = Queue()
    message_count = 0
    start_time = time()
    message_queue_thread = threading.Thread(target=ipfs.subscribe, args=(subtopic, message_queue), name='message_queue_thread', daemon=True)
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
                server.process_ipfs_sub_message(message)
        
        if not message_queue_thread.is_alive():
            if not(ipfs_subscribe_timeout):
                exit_with_error(f'An error occurred monitoring the message queue for topic {subtopic}.')
            else:
                debug('Restarting IPFS subscription after timeout.')
                message_queue_thread = threading.Thread(target=ipfs.subscribe, args=(subtopic, message_queue), name='message_queue_thread', daemon=True)
                message_queue_thread.start()
        
        running_time = time() - start_time
        if int(running_time) % 60 == 0:
            log_message = f'maude server running in subscribe mode for {timedelta(seconds=int(running_time))}. Processed {message_count} total messages. Press [ENTER] to shutdown.'
            if not log_message == last_log_message: 
                info(f'maude server running in subscribe mode for {timedelta(seconds=int(running_time))}. Processed {message_count} total messages. Press [ENTER] to shutdown.')
                last_log_message = log_message
    info("maude server shutdown.")

@servercmd.command(help='Monitor a local IPFS instance for pin requests for CIDs.')  
@click.option('--id', default='maude', help='The maude instance id.')
@click.option('--ipfs-node', default='/dns/localhost/tcp/5001/http', help='The address of the IPFS node API to connect to.')
@click.option('--keyfile', default='[id].pem', help='The private-key file to use.')
@click.argument('log-file', type=click.Path(exists=True), default='ipfs.log')
def monitor(id, ipfs_node, keyfile, log_file):
    maude_global.MAUDE_ID = id
    info(f'Maude instance id is {id}.')
    init_ipfs_client(ipfs_node)
    if keyfile == '{instance_id}.pem':
        keyfile = id + '.pem'
    if not os.path.exists(keyfile):
        exit_with_error(f'The private key file {keyfile} does not exist. Run `maude crypto gen` to generate a public/private-key pair.')
    with begin(f'Loading private key from {keyfile}') as op:
        crypto.load_private_key(keyfile)
        op.complete()
    pubtopic = id
    info(f'Reading IPFS log file {log_file}...')
    info(f'Publishing to IPFS topic {pubtopic}...')
    
    with begin('Loading classifiers') as op:
        server.yara_classifier = binary.yara_classifier.Classifier('binaryalert')
        server.clamAVAvailable = binary.clamav_classifier.libraryAvailable()
        if server.clamAVAvailable:
            server.clamav_classifier = binary.clamav_classifier.Classifier()
        else:
            error('ClamAV not available. Check that libclamav libraries are installed.')
        server.nsfw_classifier = image.nfsw_classifier.Classifier()
        server.nudenet_image_classifier = image.nudenet_classifier.Classifier()
        server.nudenet_video_classifier = video.nudenet_classifier.Classifier()
        server.photoDNAHashAvailable = image.ms_photodna.libraryAvailable()
        op.complete()

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
                if server.process_ipfs_log_entry(message):
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