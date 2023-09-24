from starknet_py.net.models.chains import StarknetChainId

ENDLESS_MENU = True

WALLETS_TO_GENERATE_COUNT = 1

GENERATED_WALLETS_JSON_PATH = "data/internal/generated_wallets.json"
DEPLOYED_WALLETS_TXT_PATH = "data/internal/deployed_wallets.txt"
DEPLOY_FAILED_WALLETS_JSON_PATH = "data/internal/deploy_failed_wallets.json"

# путь к файлу с прокси
PROXIES_TXT_PATH = "data/proxies.txt"

# если вы используете прокси, то ставить True, в противном случае - False
USE_PROXY = False

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
SHOULD_WITHDRAW_FOR_DEPLOY = False
WITHDRAW_FOR_DEPLOY_ETH_AMOUNT = (0.00001, 0.00001)

WAIT_FOR_TOPUP_FROM_CEX_IN_SEC = 10
WAIT_FOR_TOPUP_FROM_CEX_ATTEMPTS = -1  # если меньше 0, то бесконечно

STARKNET_NETWORK = "mainnet"  # testnet | testnet2 | mainnet
STARKNET_CHAIN_ID = StarknetChainId.MAINNET  # | TESTNET | TESTNET2 | MAINNET

CLIENT_ON_ERROR_TOTAL_TRIES = 5
CLIENT_ON_ERROR_SLEEP_IN_SEC = 20

GAS_THRESHOLD = 40
GAS_DELAY_RANGE = [10, 15]