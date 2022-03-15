from logging import info, error, debug
from multibase import encode, decode
def process_forum_message(msg):
    peer:str = msg['from']
    seqno = decode(msg['seqno'])
    topicIDs = list(map(lambda t: decode(t).decode('UTF-8'), msg['topicIDs']))
    try:
        data:str = decode(msg['data']).decode('UTF-8')
    except UnicodeDecodeError as e:
        error(f'Message data from peer {peer} with seqno {seqno} is not UTF-8 encoded Unicode text. Skipping.')
        return False
    except Exception as e:
        error(f'Error decoding message data from peer {peer} with seqno {seqno}: {e}')
        return False
    return True