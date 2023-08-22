from starknet_py.net.models.chains import StarknetChainId

ENDLESS_MENU = True

WALLETS_TO_GENERATE_COUNT = 5

GENERATED_WALLETS_JSON_PATH = "data/internal/generated_wallets.json"
DEPLOYED_WALLETS_TXT_PATH = "data/internal/deployed_wallets.txt"
DEPLOY_FAILED_WALLETS_JSON_PATH = "data/internal/deploy_failed_wallets.json"

WALLETS_EXCEL_PATH = "data/wallets.xlsx"

LOAD_OKX_API_CONFIG_FROM_ENV = False

OKX_API_CONFIG = {
    'apiKey': '',
    'secret': '',
    'password': '',
    'enableRateLimit': True
}


CEX_WITHDRAW_FEE = 0.0001

DEPLOY_SLEEP_DEVIATION_IN_SEC = (1, 5)
SHOULD_WITHDRAW_FOR_DEPLOY = True
WITHDRAW_FOR_DEPLOY_ETH_AMOUNT = (0.00001, 0.00001)

WAIT_FOR_TOPUP_FROM_CEX_IN_SEC = 10
WAIT_FOR_TOPUP_FROM_CEX_ATTEMPTS = -1  # если меньше 0, то бесконечно

STARKNET_NETWORK = "mainnet"  # testnet | testnet2 | mainnet
STARKNET_CHAIN_ID = StarknetChainId.MAINNET  # | TESTNET | TESTNET2 | MAINNET
