import click

from cli.commands import crypto

@crypto.command('gen', help='Generate public/private key pairs for maude.')
@click.argument('privkey', default='maude.pem')
@click.argument('pubkey', default='maude_pub.pem')
def crypto_generate_keys(privkey, pubkey):
   from core.crypto import generate_rsa_key_pair
   generate_rsa_key_pair(privkey, pubkey)
