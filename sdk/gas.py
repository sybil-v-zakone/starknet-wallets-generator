import random
import time
from functools import wraps

from loguru import logger
from web3 import Web3

from constants import ETH_MAINNET_RPC
from progress.bar import IncrementalBar


def gas_delay(gas_threshold: int, delay_range: list):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            while True:
                current_eth_gas_price = get_eth_gas_fee()
                threshold = Web3.to_wei(gas_threshold, "gwei")
                logger.info(current_eth_gas_price)
                logger.info(threshold)
                if current_eth_gas_price > threshold:
                    random_delay = random.randint(delay_range[0], delay_range[1])

                    logger.warning(
                        f"Current gas fee '{current_eth_gas_price}' wei > Gas threshold '{threshold}' wei. Waiting for {random_delay} seconds..."
                    )

                    bar = IncrementalBar('Waiting:', max=random_delay)
                    for _ in range(random_delay):
                        time.sleep(1)
                        bar.next()
                else:
                    break

            return func(*args, **kwargs)

        return wrapper

    return decorator


def get_eth_gas_fee():
    w3 = Web3(Web3.HTTPProvider(ETH_MAINNET_RPC))
    return w3.eth.gas_price
