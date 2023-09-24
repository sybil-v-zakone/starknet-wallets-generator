from config import (
    GENERATED_WALLETS_JSON_PATH,
    DEPLOYED_WALLETS_TXT_PATH,
    DEPLOY_FAILED_WALLETS_JSON_PATH
)

ACCOUNT_CLASS_HASH = 0x1a736d6ed154502257f02b1ccdf4d9d1089f80811cd6acad48e6b6a9d1f2003

GRIND_KEY_MAX_ALLOWED_VALUE = "f80000000000020efffffffffffffff738a13b4b920e9411ae6da5f40b0358b1"
GRIND_KEY_VALUE_LIMIT = "800000000000010ffffffffffffffffb781126dcae7b2321e66a241adc64d2f"

BASE_DERIVATION_PATH = "m/44'/9004'/0'/0/0"

ETH_MAINNET_RPC = "https://rpc.ankr.com/eth"
ETH_STARKNET_TOKEN_ADDRESS = 0x049D36570D4E46F48E99674BD3FCC84644DDD6B96F7C741B1562B82F9E004DC7

OKX_WITHDRAW_OPTIONS = {
    "dest": {
        "INTERNAL_TRANSFER": 3,
        "ON_CHAIN": 4
    },
    "network": "Starknet",
    "symbol_withdraw": "ETH"
}

WALLET_EXPORT_SHEETS = {
    'Generated wallets': GENERATED_WALLETS_JSON_PATH,
    'Deployed wallets': DEPLOYED_WALLETS_TXT_PATH,
    'Failed to deploy wallets': DEPLOY_FAILED_WALLETS_JSON_PATH
}

STARKSCAN_URL = 'https://starkscan.co/tx'
