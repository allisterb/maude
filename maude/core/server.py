import json

from logging import info, error, debug
from multibase import encode, decode

from filetype import guess, get_bytes

from core.ipfs import get_file

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
    return True

def process_log_entry(msg):
    log_entry = json.loads(msg)
    file_hash = ''
    if log_entry['msg'].startswith('announce - start - '):
        file_hash = log_entry['msg'].replace('announce - start - ', '')
    else:
        return False
    info(f'File to be analyzed is {file_hash}.')
    f:bytes = get_file(file_hash)
    debug(f'File is {f}')
    file_type = guess(get_bytes(f))
    info(f'File has type {file_type}.')


