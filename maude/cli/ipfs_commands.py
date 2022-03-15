import click
from rich import print
from pyipfs import ipfshttpclient

from base.timer import begin
from cli.commands import ipfs as ipfscmd
from cli.util import *
from core import ipfs

def init_ipfs_client(api_url):
    with begin("Connecting to IPFS node") as op:
        ipfs.ipfsclient = ipfshttpclient.connect(session=True)
        op.complete()

@ipfscmd.command('info')
def ipfs_info():
    init_ipfs_client()
    print(ipfs.get_client_id())
