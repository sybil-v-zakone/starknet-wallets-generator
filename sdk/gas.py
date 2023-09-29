import random
import time
from functools import wraps

from loguru import logger
from web3 import Web3

from progress.bar import IncrementalBar
from sdk.apis.gas_api import GasAPI


def gas_delay(gas_threshold: int, delay_range: list):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            gas_api = GasAPI(proxy=self.proxy)
            while True:
                current_starknet_gas_price = gas_api.get_last_block_gas_price()
                threshold = Web3.to_wei(gas_threshold, "gwei")
                logger.info(current_starknet_gas_price)
                logger.info(threshold)
                if current_starknet_gas_price > threshold:
                    random_delay = random.randint(delay_range[0], delay_range[1])

                    logger.warning(
                        f"Current STARKNET gas fee '{current_starknet_gas_price}' wei > Gas threshold '{threshold}' wei. Waiting for {random_delay} seconds..."
                    )

                    bar = IncrementalBar('Waiting:', max=random_delay)
                    for _ in range(random_delay):
                        time.sleep(1)
                        bar.next()
                else:
                    break
            gas_api.close_session()
            return func(self, *args, **kwargs)

        return wrapper

    return decorator
