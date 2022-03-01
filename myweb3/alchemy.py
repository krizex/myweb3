from .connection import build_web3
from .config import Config
from .sendmail import send_mail
from .contracts import compile_file
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
def test_send_email():
    send_mail('A test mail', 'the content')


@cli.command()
@click.argument('address')
@click.argument('amount')
def send_tx(address, amount):
    account = w3.eth.account.from_key(Config["PRIVATE_KEY"])
    tx = {
        "nonce": w3.eth.getTransactionCount(account.address),
        "to": address,
        "value": w3.toWei(amount, "ether"),
        "gas": 21000,
        "gasPrice": w3.toWei("2", "gwei")
    }
    log.info("Send to %s: %s", address, tx)
    signed_tx = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    log.info("Tx address: %s", tx_hash.hex())


@cli.command()
@click.argument("contract_file")
def deploy_contract(contract_file):
    contract_compiled = compile_file(contract_file)
    log.info("Contract: %s", contract_compiled)
    contract_name = "HelloWorld"
    log.info("Using contract=%s", contract_name)
    contract_interface = contract_compiled[contract_file + ":" + contract_name]
    contract = w3.eth.contract(abi=contract_interface["abi"], bytecode=contract_interface["bin"])
    myaccount = w3.eth.account.from_key(Config["PRIVATE_KEY"])
    # FIXME: should update to use send_raw_transaction
    tx_params = {
        "nonce": w3.eth.getTransactionCount(myaccount.address),
    }
    ctor_param = "My First Message"
    log.info("Calling contract ctor with: %s", ctor_param)
    tx = contract.constructor(ctor_param).buildTransaction(tx_params)
    signed_tx = myaccount.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    log.info("TxHash: %s", tx_hash.hex())
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    log.info("TxReceipt: %s", tx_receipt)
    addr = tx_receipt['contractAddress']
    log.info('Deploy to %s', addr)
    return addr



