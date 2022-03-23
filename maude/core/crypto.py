from logging import info

from Crypto.PublicKey import RSA

from base.timer import begin

def generate_rsa_key_pair(private_key_filename='maude.pem', public_key_filename='maude_public.pem'):
    with begin('Generating RSA key-pair') as op:
        keypair = RSA.generate(2048)
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
    
