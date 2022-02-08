import logging
from web3 import Web3
from web3.middleware import geth_poa_middleware

from .config import Config

log = logging.getLogger(__name__)


def build_web3():
    return _build_web3(Config)


def _build_web3(cfg):
    url = cfg["API_KEY"]
    log.info('Connecting to %s', url)
    w3 = Web3(Web3.HTTPProvider(url))
    if cfg.get_bool("POA"):
        log.info("It is a POA chain")
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return w3
