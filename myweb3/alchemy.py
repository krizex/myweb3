from .connection import build_web3
import click
import logging

log = logging.getLogger(__name__)
w3 = build_web3()


@click.group()
def cli():
    pass


@cli.command()
@click.argument("index", default="latest")
def get_block(index):
    log.info('Getting block %s', index)
    blk = w3.eth.get_block(index)
    print(blk)


@cli.command()
def foo():
    print('foo')


@cli.command()
def bar():
    print('bar')
