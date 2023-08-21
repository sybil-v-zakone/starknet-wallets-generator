import time

from loguru import logger
from starknet_py.hash.selector import get_selector_from_name
from starknet_py.net.account.account import Account
from starknet_py.net.client_models import Call

import config
from constants import ETH_STARKNET_TOKEN_ADDRESS


async def wait_for_topup(initial_balance, chain, client, address, key_pair,
                         attempts=config.WAIT_FOR_TOPUP_FROM_CEX_ATTEMPTS):
    current_balance = await check_account_balance(chain, client, address, key_pair)
    logger.info(f"Initial balance: {initial_balance[0]} / {initial_balance[1]}")
    logger.info(f"Current balance: {current_balance[0]} / {current_balance[1]}")
    if current_balance[0] <= initial_balance[0]:
        if attempts > 0 or attempts == -1:
            logger.info(f"Waiting for topup on {address}. Sleep is {config.WAIT_FOR_TOPUP_FROM_CEX_IN_SEC}")
            time.sleep(config.WAIT_FOR_TOPUP_FROM_CEX_IN_SEC)
            return await wait_for_topup(
                initial_balance,
                chain,
                client,
                address,
                key_pair,
                attempts - 1 if attempts != -1 else -1
            )
        else:
            logger.error(f"Reached maximum attempts, topup failed on {address}")
            return False
    else:
        logger.success(f"Topup on {address} successfull")
        return True


async def check_account_balance(chain, client, address, key_pair):
    account = Account(
        address=address,
        key_pair=key_pair,
        chain=chain,
        client=client
    )

    call = Call(
        to_addr=ETH_STARKNET_TOKEN_ADDRESS,
        selector=get_selector_from_name("balanceOf"),
        calldata=[account.address],
    )

    return await account.client.call_contract(call)
