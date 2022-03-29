import click
from rich import print
from pyipfs import ipfshttpclient

from base.timer import begin
from cli.commands import ipfs as ipfscmd
from cli.util import *
from core import ipfs

def init_ipfs_client(api_url=None):
    with begin("Connecting to IPFS node") as op:
        ipfs.ipfsclient = ipfshttpclient.connect(session=True) if api_url == '/dns/localhost/tcp/5001/http' else ipfshttpclient.connect(addr=api_url, session=True)
        op.complete()
        
@ipfscmd.command('info', help='Print out maude IPFS client info.')
@click.option('--ipfs-node', default='/dns/localhost/tcp/5001/http')
def ipfs_info(ipfs_node):
    init_ipfs_client(ipfs_node)
    print(ipfs.get_client_id())

@ipfscmd.command('config', help='Print out IPFS server configuration.')
@click.option('--ipfs-node', default='/dns/localhost/tcp/5001/http')
@click.argument('key', required=False)
def ipfs_config(ipfs_node, key):
    init_ipfs_client(ipfs_node)
    c = ipfs.get_config(key)
    if c != None:
        print(c)
