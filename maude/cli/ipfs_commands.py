import click
from rich import print
from pyipfs import ipfshttpclient

from base.timer import begin
from cli.commands import ipfs as ipfscmd
from cli.util import *
from core import ipfs

def init_ipfs_client(api_url=None):
    with begin("Connecting to IPFS node") as op:
        try:
            ipfs.ipfsclient = ipfshttpclient.connect(session=True)
            op.complete()
        except ConnectionError as ce:
            op.abandon()
            exit_with_error(f'Error connecting to IPFS API: {ce}')

@ipfscmd.command('info')
def ipfs_info():
    init_ipfs_client()
    print(ipfs.get_client_id())

@ipfscmd.command('config')
@click.argument('key', required=False)
def ipfs_config(key):
    init_ipfs_client()
    c = ipfs.get_config(key)
    if c != None:
        print(c)
