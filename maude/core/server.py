import os
import json

from logging import info, error, debug
from tempfile import TemporaryDirectory

from multibase import decode as multi_decode, encode
from filetype import guess_extension, get_bytes, is_archive, is_image, is_video

from base.runtime import serialize_to_json
from core.ipfs import get_file, is_file_or_dir, publish
from core.crypto import sign_PKCS1
from binary.clamav_classifier import Classifier as ClamAVClassifier
from binary.yara_classifier import Classifier as YARAClassifier
from text.perspective_classifier import TextClassifier as PerspectiveTextClassifier
from image.nfsw_classifier import Classifier as NsfwClassifier
from image.nudenet_classifier import Classifier as NudeNetImageClassifier
from video.nudenet_classifier import Classifier as NudeNetVideoClassifier
from image.ms_photodna import generateHash

clamav_classifier: ClamAVClassifier = None
yara_classifier: YARAClassifier = None
nsfw_classifier: NsfwClassifier = None
nudenet_image_classifier: NudeNetImageClassifier = None
nudenet_video_classifier: NudeNetVideoClassifier = None
perspective_classifier: PerspectiveTextClassifier = None
photoDNAHash = False

def process_sub_message(msg, pubtopic):
    global nsfw_classifier
    global nudenet_classifier
    global perspective_classifier
    
    peer:str = msg['from']
    seqno = multi_decode(msg['seqno'])
    topicIDs = list(map(lambda t: multi_decode(t).decode('UTF-8'), msg['topicIDs']))
    data:str = ''
    try:
        data = multi_decode(msg['data']).decode('UTF-8')
    except UnicodeDecodeError as e:
        error(f'Message data from peer {peer} with seqno {seqno} is not UTF-8 encoded Unicode text. Skipping.')
        return False
    except Exception as e:
        error(f'Error decoding message data from peer {peer} with seqno {seqno}: {e}')
        return False
    if not perspective_classifier is None:
        per_data = perspective_classifier.classify(data)
        publish(str(encode('base64url', pubtopic), 'utf-8'), json.dumps(per_data).encode('utf-8'))
    else:
        info('Not using Google Perspective API.')
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
            file_type_ext = 'unknown_bin'
    info(f'{file_hash} has type {file_type_ext} and length {len(file_bytes)} bytes.')
    file_is_archive = is_archive(file_header)
    file_is_image = is_image(file_header)
    file_is_video = is_video(file_header)
    with TemporaryDirectory() as td:
        file_name = os.path.join(td, file_hash)
        with open(file_name, 'wb') as fh:
            fh.write(file_bytes)
        debug(f'Created temporary file: {file_name}.')
    
        if file_type_ext == 'txt':
            data = yara_classifier.classify(file_name)
            info(f'YARA classification for binary {file_hash}: {data}')
            publish(str(encode('base64url', pubtopic), 'utf-8'), json.dumps(data).encode('utf-8'))

        elif file_is_image:
            data = {**nudenet_image_classifier.classify(file_name), **nsfw_classifier.classify(file_name)}
            if (photoDNAHash):
                data['photoDNA'] = generateHash(file_name)
            info(f'NudeNet and nsfw_model classification data for image {file_hash}: {data}')
            publish(str(encode('base64url', pubtopic), 'utf-8'), json.dumps(data).encode('utf-8'))
            os.remove(file_name)

        elif file_is_video:
            data = nudenet_video_classifier.classify(file_name)
            info(f'NudeNet classification data for video {file_hash}: {data}')
            publish(str(encode('base64url', pubtopic), 'utf-8'), serialize_to_json(data).encode('utf-8'))

        else:
            data = yara_classifier.classify(file_name)
            info(f'YARA classification data for binary {file_hash}: {data}')
            publish(str(encode('base64url', pubtopic), 'utf-8'), json.dumps(data).encode('utf-8'))
            data = clamav_classifier.classify(file_name)
            info(f'ClamAV classification data for binary {file_hash}: {data}')
            publish(str(encode('base64url', pubtopic), 'utf-8'), json.dumps(data).encode('utf-8'))
            os.remove(file_name)
            publish(str(encode('base64url', pubtopic), 'utf-8'), json.dumps(data).encode('utf-8'))
        
          
            



