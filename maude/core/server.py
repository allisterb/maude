import json

from logging import info, error, debug
from multibase import encode, decode

from filetype import guess, guess_extension, get_bytes, is_image, is_video

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



