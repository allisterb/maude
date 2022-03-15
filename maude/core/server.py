from logging import info
from multibase import encode,decode
def process_forum_message(msg):
    peer:str = msg['from']
    data:str = str(decode(msg['data']), 'utf-8')
    seqnos:str = str(decode(msg['seqno'], 'utf-8'))
    topicIDs: list[str] = msg['topicIDs']
    info(data)
    