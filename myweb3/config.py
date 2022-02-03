from dotenv import dotenv_values
import logging

log = logging.getLogger(__name__)


def load_env():
    envs = dotenv_values(".env")

    log.info("Config: %s", envs)

    return envs
