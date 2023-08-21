from ccxt import okx
from loguru import logger

from config import OKX_API_CONFIG, CEX_WITHDRAW_FEE, LOAD_OKX_API_CONFIG_FROM_ENV
from constants import okx_constants
from sdk.load_from_env import load


def get_config():
    if LOAD_OKX_API_CONFIG_FROM_ENV:
        return load()
    return OKX_API_CONFIG


def okx_withdraw(
        to_address: str,
        amount_to_withdrawal: float
) -> bool:
    exchange_config = get_config()
    exchange = okx(exchange_config)
    try:
        chain_name = f"{okx_constants['symbol_withdraw']}-{okx_constants['network']}"
        logger.info(f"Withdraw {amount_to_withdrawal} {chain_name} from OKX to {to_address}")
        exchange.withdraw(
            okx_constants['symbol_withdraw'],
            amount_to_withdrawal,
            to_address,
            params={
                "toAddress": to_address,
                "chain": chain_name,
                "dest": okx_constants["dest"]["ON_CHAIN"],
                "fee": CEX_WITHDRAW_FEE,
                "pwd": '-',
                "amt": amount_to_withdrawal,
                "network": okx_constants['network']
            })

        logger.success(f"[OKX] withdraw {amount_to_withdrawal} {chain_name}")
        return True
    except Exception as e:
        logger.error(f"[OKX] withdraw {amount_to_withdrawal} error: {str(e)}")
        return False
