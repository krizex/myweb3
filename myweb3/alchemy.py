from .connection import build_web3
from .config import Config
from .sendmail import send_mail
import click
import logging
import time

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
def get_block_number():
    n = w3.eth.get_block_number()
    print(n)


@cli.command()
def send_tx():
    pass


@cli.command()
@click.argument("address", default="")
def get_account_balance(address):
    if address == "":
        account = w3.eth.account.from_key(Config["PRIVATE_KEY"])
        address = account.address
    balance = w3.eth.get_balance(address)
    print(balance)


def _mine_address():
    account = w3.eth.account.create()
    balance = w3.eth.get_balance(account.address)
    account_priv_key = account.key.hex()
    if balance != 0:
        print("Find account=%s, balance=%d" % (account_priv_key, balance))
        content = "Account=%s, balance=%s" % (account_priv_key, balance)
        send_mail("Find an account", content)

    return account_priv_key


@cli.command()
def mine_address():
    cnt = 0
    while True:
        cnt += 1
        try:
            priv_key = _mine_address()
            log.info('[%d]Mining %s', cnt, priv_key)
        except:
            log.exception("Fails to mine")
            time.sleep(0.1)


@cli.command()
def send_email():
    send_mail('A test mail', 'the content')
