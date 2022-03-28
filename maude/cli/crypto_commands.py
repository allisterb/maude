import binascii
from logging import info

import click

import core.crypto
from cli.commands import crypto

@crypto.command('gen', help='Generate a RSA 2048-bit public/private key pair for maude.')
@click.argument('privkey', default='maude.pem')
@click.argument('pubkey', default='maude_pub.pem')
def crypto_generate_keys(privkey, pubkey):
   from core.crypto import generate_rsa_key_pair
   generate_rsa_key_pair(privkey, pubkey)

@crypto.command('sign', help='Generate a RSA 2048-bit public/private key pair for maude.')
@click.argument('message')
@click.argument('keyfile', type=click.Path(exists=True), default='maude.pem')
def crypto_sign(message, keyfile):
   core.crypto.load_private_key(keyfile)
   s = binascii.b2a_base64(core.crypto.sign_PKCS1(message))
   info (f'PKCS#1 signature for {message} is {s}.')

