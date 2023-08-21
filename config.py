from starknet_py.net.models.chains import StarknetChainId

ENDLESS_MENU = True

WALLETS_TO_GENERATE_COUNT = 5
GENERATED_WALLETS_JSON_PATH = "data/generated_wallets.json"
GENERATED_WALLETS_EXCEL_PATH = "data/generated_wallets.xlsx"

DEPLOY_SLEEP_DEVIATION_IN_SEC = (1, 5)

DEPLOYED_WALLETS_TXT_PATH = "data/deployed_wallets.txt"
DEPLOYED_WALLETS_EXCEL_PATH = "data/deployed_wallets.xlsx"

DEPLOY_FAILED_WALLETS_EXCEL_PATH = "data/deploy_failed_wallets.xlsx"
DEPLOY_FAILED_WALLETS_JSON_PATH = "data/deploy_failed_wallets.json"

LOAD_OKX_API_CONFIG_FROM_ENV = False

OKX_API_CONFIG = {
    'apiKey': '',
    'secret': '',
    'password': '',
    'enableRateLimit': True
}

CEX_WITHDRAW_FEE = 0.0001

SHOULD_WITHDRAW_FOR_DEPLOY = True
WITHDRAW_FOR_DEPLOY_ETH_AMOUNT = 0.00001

WAIT_FOR_TOPUP_FROM_CEX_IN_SEC = 10
WAIT_FOR_TOPUP_FROM_CEX_ATTEMPTS = -1  # если меньше 0, то бесконечно

STARKNET_NETWORK = "mainnet"  # testnet | testnet2 | mainnet
STARKNET_CHAIN_ID = StarknetChainId.MAINNET  # | TESTNET | TESTNET2 | MAINNET
