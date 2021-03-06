from logging import info, debug

from Crypto.PublicKey.RSA import RsaKey, generate, import_key
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256
import binascii

from base.timer import begin

private_key:RsaKey = None
public_key:RsaKey = None

def generate_rsa_key_pair(private_key_filename, public_key_filename):
    with begin('Generating RSA 2048-bit key-pair') as op:
        keypair = generate(2048)
        private_key = keypair.export_key('PEM')
        public_key = keypair.public_key().export_key('PEM')
        with open(private_key_filename, "wb") as f:
            f.write(private_key)
            f.close()
        info(f'Wrote private key in PEM format to {private_key_filename}.')
        
        with open(public_key_filename, "wb") as f:
            f.write(public_key)
            f.close()
        info(f'Wrote public key in PEM format to {public_key_filename}.')
        op.complete()
    
def load_private_key(keyfile):
    global private_key
    with open(keyfile, 'rb') as f:
         private_key = import_key(f.read())

def sign_PKCS1(msg):
    assert(private_key is not None)
    with begin('Signing message using PKCS#1 scheme') as op:
        hash = SHA256.new(msg)
        signer = PKCS115_SigScheme(private_key)
        signature = signer.sign(hash)
        debug("Message signature:", binascii.b2a_base64(signature))
        op.complete()
        return signature