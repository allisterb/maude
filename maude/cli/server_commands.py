from time import time, sleep
from logging import info, error, debug

import click
from rich import print

from pyipfs import ipfshttpclient

from base.timer import begin
from core import ipfs
from cli.commands import server
from maude_global import KBINPUT

def init_ipfs_client(api_url):
    with begin("Connecting to IPFS node") as op:
        ipfs.ipfsclient = ipfshttpclient.connect(session=True)
        op.complete()

@server.command('run')  
@click.option('--ipfs-node')
@click.argument('forum')
def run(ipfs_node, forum:str):
    init_ipfs_client(ipfs_node)
    sub = ipfs.ipfsclient.pubsub.subscribe(forum, False)
    start_time = time()
    while (not KBINPUT):
        message_count = 0
        for message in sub:
            print(message)
            message_count += 1
        running_time = "{:0.2f}".format(time() - start_time)
        info(f'maud3 server running for {running_time} s. Processed {message_count} messages.')
        sleep(1)
    

