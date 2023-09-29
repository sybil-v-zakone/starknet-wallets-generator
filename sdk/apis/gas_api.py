import time

import requests
from loguru import logger

from config import USE_PROXY
from constants import STARKNET_GET_LAST_BLOCK_ENDPOINT


class GasAPI:
    def __init__(self, proxy: str) -> None:
        self.proxy = proxy
        self.session = self.get_session()

    def get_session(self) -> requests.Session:
        session = requests.Session()
        if USE_PROXY:
            proxy_url = f"http://{self.proxy}"
            session.proxies = {"https": proxy_url}

        return session
    
    def close_session(self):
        if self.session:
            self.session.close()

    def get_last_block_gas_price(self):
        while True:
            try:
                response = self.session.get(url=STARKNET_GET_LAST_BLOCK_ENDPOINT)
                gas_price_hex = response.json()["gas_price"]

                return int(gas_price_hex, 16)
            except Exception as e:
                logger.warning(f"Starknet gas price fetch error: {str(e)}. Retrying in 30 sec")
                time.sleep(30)
