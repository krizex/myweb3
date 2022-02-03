from .config import load_env
from web3 import Web3

cfg = load_env()
w3 = Web3(Web3.HTTPProvider(cfg["API_KEY"]))


def get_block(idx="latest"):
    return w3.eth.get_block(idx)
