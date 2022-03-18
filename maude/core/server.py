import os
import json

from logging import info, error, debug
from tempfile import TemporaryDirectory
from xmlrpc.client import Boolean
from multibase import decode, encode
from filetype import guess_extension, get_bytes, is_image, is_video

from core.ipfs import get_file, get_object, is_file_or_dir, publish
from image.nfsw_classifier import Classifier

def process_forum_message(msg):
    peer:str = msg['from']
    seqno = decode(msg['seqno'])
    topicIDs = list(map(lambda t: decode(t).decode('UTF-8'), msg['topicIDs']))
    data:str = ''
    try:
        data = decode(msg['data']).decode('UTF-8')
    except UnicodeDecodeError as e:
        error(f'Message data from peer {peer} with seqno {seqno} is not UTF-8 encoded Unicode text. Skipping.')
        return False
    except Exception as e:
        error(f'Error decoding message data from peer {peer} with seqno {seqno}: {e}')
        return False
    debug(topicIDs)
    debug(data)
    return True

def process_log_entry(msg, pubtopic) -> bool:
    log_entry = json.loads(msg)
    file_hash = ''
    if log_entry['logger'] =='bitswap' and log_entry['msg'] == 'Bitswap.ProvideWorker.Start':
        debug(f'Log entry read: {msg}')
        cid = log_entry['cid']
        if is_file_or_dir(cid):
            info(f'File or directory {cid} requested by local node or by network.')
            return True
        else:
            return False
    elif log_entry['msg'].startswith('announce - start - '):
        debug(f'Log entry read: {msg}')
        file_hash = log_entry['msg'].replace('announce - start - ', '')
        info(f'File {file_hash} pinned locally.')
    else:
        return False
    info(f'File to be analyzed is {file_hash}.')
    file_bytes:bytes = get_file(file_hash)
    file_text:str = ''
    file_header = get_bytes(file_bytes)
    file_type_ext = guess_extension(file_header)
    if (file_type_ext == None):
        try:
            file_text = file_bytes.decode('utf-8')
            info('The file can be decoded as UTF-8...assuming file type is txt.')
            file_type_ext = 'txt'
        except UnicodeDecodeError as _:
            error(f'Could not determine the file type of {file_hash}. Skipping.')
            return False
    info(f'{file_hash} has type {file_type_ext} and length {len(file_bytes)} bytes.')
    file_is_image = is_image(file_header)
    file_is_video = is_video(file_header)
    with TemporaryDirectory() as td:
        file_name = os.path.join(td, file_hash)
        with open(file_name, 'wb') as fh:
            fh.write(file_bytes)
        debug(f'Created temporary file: {file_name}.')
        if file_is_image:
            classifier = Classifier(file_name)
            data =list(classifier.classify().values())[0] 
            info(f'Classification for image {file_hash}: {data}')
            classifier.image.close()
            os.remove(file_name)
            publish(str(encode('base64url', pubtopic), 'utf-8'), json.dumps(data).encode('utf-8'))
            



