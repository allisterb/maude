# Based on https://github.com/jankais3r/pyPhotoDNA/blob/main/generateHashes.py

import os
import sys
import glob
import time
import base64
import multiprocessing
from logging import info, error

from ctypes import cast
from ctypes import cdll
from ctypes import c_int
from ctypes import c_ubyte
from ctypes import POINTER
from ctypes import c_char_p

from PIL import Image
def libraryAvailable(lib_path=None):
    if lib_path is None:
        if sys.platform == "win32":
            lib_path = 'PhotoDNAx64.dll'
        elif sys.platform == "darwin":
            lib_path = 'PhotoDNAx64.so'
        else: 
            raise Exception('Linux is not supported by PhotoDNA.')
    try:
        libPhotoDNA = cdll.LoadLibrary(lib_path)
        return True
    except OSError as e:
        return False

def generateHash(image_source, lib_path=None) -> bytes:
    if lib_path is None:
        if sys.platform == "win32":
            lib_path = 'PhotoDNAx64.dll'
        elif sys.platform == "darwin":
            lib_path = 'PhotoDNAx64.so'
        else: 
            raise Exception('Linux is not supported by PhotoDNA.')
    imageFile = Image.open(image_source, 'r')
    if imageFile.mode != 'RGB':
        imageFile = imageFile.convert(mode = 'RGB')
    libPhotoDNA = cdll.LoadLibrary(lib_path)

    ComputeRobustHash = libPhotoDNA.ComputeRobustHash
    ComputeRobustHash.argtypes = [c_char_p, c_int, c_int, c_int, POINTER(c_ubyte), c_int]
    ComputeRobustHash.restype = c_ubyte

    hashByteArray = (c_ubyte * 144)()
    ComputeRobustHash(c_char_p(imageFile.tobytes()), imageFile.width, imageFile.height, 0, hashByteArray, 0)

    hashPtr = cast(hashByteArray, POINTER(c_ubyte))
    hashList = [str(hashPtr[i]) for i in range(144)]
    hashString = ','.join([i for i in hashList])
    hashList = hashString.split(',')
    for i, hashPart in enumerate(hashList):
        hashList[i] = int(hashPart).to_bytes((len(hashPart) + 7) // 8, 'big')
    hashBytes = b''.join(hashList)
    return base64.b64encode(hashBytes).decode('utf-8')

    #outputFile.write('"' + imagePath + '","' + hashString + '"\n')