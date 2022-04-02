import os
import json

from logging import info, error, debug
from tempfile import TemporaryDirectory

from multibase import decode as multi_decode, encode
from filetype import guess_extension, get_bytes, is_archive, is_image, is_video

from base.runtime import serialize_to_json_str
from core.ipfs import get_file, is_file_or_dir, publish
from core.crypto import sign_PKCS1
from binary.clamav_classifier import Classifier as ClamAVClassifier
from binary.yara_classifier import Classifier as YARAClassifier
from text.perspective_classifier import TextClassifier as PerspectiveTextClassifier
from image.nfsw_classifier import Classifier as NsfwClassifier
from image.nudenet_classifier import Classifier as NudeNetImageClassifier
from image.ms_photodna import generateHash
from video.nudenet_classifier import Classifier as NudeNetVideoClassifier

clamav_classifier: ClamAVClassifier = None
yara_classifier: YARAClassifier = None
nsfw_classifier: NsfwClassifier = None
nudenet_image_classifier: NudeNetImageClassifier = None
nudenet_video_classifier: NudeNetVideoClassifier = None
perspective_classifier: PerspectiveTextClassifier = None
photoDNAHashAvailable = False
clamAVAvailable = False

def process_sub_message(msg, pubtopic):
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
        publish(str(encode('base64url', pubtopic), 'utf-8'), serialize_to_json_str(per_data))
    else:
        info('Not using Google Perspective API.')
    return True

def process_log_entry(msg, pubtopic) -> bool:
    log_entry = json.loads(msg)
    cid = ''
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
        cid = log_entry['msg'].replace('announce - start - ', '')
        info(f'File {cid} pinned locally.')
    else:
        return False
    info(f'File to be analyzed is {cid}.')
    file_bytes:bytes = get_file(cid)
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
    info(f'{cid} has type {file_type_ext} and length {len(file_bytes)} bytes.')
    file_is_archive = is_archive(file_header)
    file_is_image = is_image(file_header)
    file_is_video = is_video(file_header)
    file_is_text = file_type_ext == 'txt'
    file_is_binary = file_type_ext == 'unknown_bin'
    file_analysis = dict()
    file_analysis['cid'] = cid
    data = dict()

    with TemporaryDirectory() as td:
        file_name = os.path.join(td, cid)
        with open(file_name, 'wb') as fh:
            fh.write(file_bytes)
        debug(f'Created temporary file: {file_name}.')
    
        if file_is_text:
            data = yara_classifier.classify(file_name)
            info(f'YARA classification for binary {cid}: {data}')
            publish(str(encode('base64url', pubtopic), 'utf-8'), serialize_to_json_str(data))

        elif file_is_image:
            data = {**nudenet_image_classifier.classify(file_name), **nsfw_classifier.classify(file_name)}
            if (photoDNAHashAvailable):
                data['photoDNA'] = generateHash(file_name)
            info(f'NudeNet and nsfw_model classification data for image {cid}: {data}')
            publish(str(encode('base64url', pubtopic), 'utf-8'), serialize_to_json_str(data))
            os.remove(file_name)

        elif file_is_video:
            data = nudenet_video_classifier.classify(file_name)
            info(f'NudeNet classification data for video {cid}: {data}')
            publish(str(encode('base64url', pubtopic), 'utf-8'), serialize_to_json_str(data))

        else:
            data = yara_classifier.classify(file_name)
            info(f'YARA classification data for binary {cid}: {data}')
            publish(str(encode('base64url', pubtopic), 'utf-8'), serialize_to_json_str(data))
            if clamAVAvailable:
                data = clamav_classifier.classify(file_name)
                info(f'ClamAV classification data for binary {cid}: {data}')
                publish(str(encode('base64url', pubtopic), 'utf-8'), serialize_to_json_str(data))
            os.remove(file_name)
            publish(str(encode('base64url', pubtopic), 'utf-8'), serialize_to_json_str(data))
        
          
            



