import logging
from collections import UserDict
from dotenv import dotenv_values

log = logging.getLogger(__name__)



class _Config(UserDict):
    def __init__(self, env_file=".env"):
        super().__init__()
        self.env_file = env_file
        self._load_env()

    def _load_env(self):
        self.data = dotenv_values(".env")

    def get_bool(self, k):
        return self.data.get("POA", '').lower() == 'true'


Config = _Config()
