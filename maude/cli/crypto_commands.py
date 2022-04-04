import binascii
from logging import info

import click

import core.crypto
from cli.commands import crypto

@crypto.command('gen', help='Generate a RSA 2048-bit public/private-key pair for a maude instance id.')
@click.option('--id', required = True, help='The maude instance id.')
def crypto_generate_keys(id):
   from core.crypto import generate_rsa_key_pair
   generate_rsa_key_pair(id + '.pem', id + '_pub.pem')

@crypto.command('sign', help='Sign a text message using the specified private key.')
@click.argument('message')
@click.argument('keyfile', type=click.Path(exists=True), default='maude.pem')
def crypto_sign(message, keyfile):
   core.crypto.load_private_key(keyfile)
   s = binascii.b2a_base64(core.crypto.sign_PKCS1(message))
   info (f'PKCS#1 signature for {message} is {s}.')