import random
import time
from datetime import datetime

from loguru import logger
from progress.bar import IncrementalBar
from starknet_py.net.client_errors import ClientError
from starknet_py.net.signer.stark_curve_signer import KeyPair
from sdk.utils import change_mobile_ip

from config import (
    GENERATED_WALLETS_JSON_PATH,
    DEPLOY_FAILED_WALLETS_JSON_PATH,
    DEPLOYED_WALLETS_TXT_PATH,
    DEPLOYED_WALLETS_JSON_PATH,
    DEPLOY_SLEEP_DEVIATION_IN_SEC,
    WITHDRAW_FOR_DEPLOY_ETH_AMOUNT,
    CEX_WITHDRAW_FEE,
    CLIENT_ON_ERROR_TOTAL_TRIES,
    CLIENT_ON_ERROR_SLEEP_IN_SEC,
    PROXIES_TXT_PATH,
    USE_PROXY,
    WALLET_APPLICATION
)
from models.wallet import Wallet
from sdk.deploy_wallet import DeployWallet
from sdk.file import (
    read_from_json,
    write_to_json,
    read_from_txt,
    write_to_txt
)


class DeployWallets:
    @staticmethod
    def get_deploy_sleep_time():
        return random.randint(*DEPLOY_SLEEP_DEVIATION_IN_SEC)

    @staticmethod
    async def deploy():
        logger.info(f"Running deploy {WALLET_APPLICATION} wallets")
        generated_wallets = read_from_json(GENERATED_WALLETS_JSON_PATH)
        previous_deploy_failed_wallets = read_from_json(DEPLOY_FAILED_WALLETS_JSON_PATH, True)
        previous_deploy_success_wallets = read_from_json(DEPLOYED_WALLETS_JSON_PATH, True)
        previous_deploy_success_wallets_addresses = []

        if isinstance(previous_deploy_success_wallets, list):
            for d in previous_deploy_success_wallets:
                if "address" in d:
                    previous_deploy_success_wallets_addresses.append(d["address"])

        current_deploy_failed_wallets = list()
        current_deploy_failed_addresses = list()
        current_deploy_success_wallets = list()
        current_deploy_success_wallets_json = list()

        current_deploy_wallets = []
        if isinstance(generated_wallets, list):
            current_deploy_wallets.extend(generated_wallets)

        if isinstance(previous_deploy_failed_wallets, list):
            current_deploy_wallets.extend(previous_deploy_failed_wallets)

        logger.info(f"Total wallets for deploy: {len(current_deploy_wallets)}")
        logger.info(
            f"All wallets will be topup for {WITHDRAW_FOR_DEPLOY_ETH_AMOUNT}ETH. CEX fee is {CEX_WITHDRAW_FEE}ETH")
        bar = IncrementalBar('Deployed wallets', max=len(current_deploy_wallets))

        proxies = read_from_txt(PROXIES_TXT_PATH)
        for index, wallet_json in enumerate(current_deploy_wallets, 1 - len(current_deploy_wallets)):
            wallet = Wallet(**wallet_json)

            if wallet.address in previous_deploy_success_wallets_addresses:
                logger.info(f"Wallet {wallet.address} already deployed. Skipping")
                continue
            if wallet.address in current_deploy_failed_addresses:
                logger.info(f"Wallet {wallet.address} already handled. Skipping")
                continue
            if wallet.address in current_deploy_success_wallets:
                logger.info(f"Wallet {wallet.address} already deployed. Skipping")
                continue

            key_pair = KeyPair.from_private_key(int(wallet.private_key, 16))
            deployer = DeployWallet(proxy=proxies[index] if USE_PROXY else None)

            change_mobile_ip()

            if USE_PROXY:
                logger.info(f'Deploying with proxy: {proxies[index]}')

            deploy_attempt = 1
            while True:
                try:
                    if deploy_attempt > CLIENT_ON_ERROR_TOTAL_TRIES:
                        logger.info("Reached maximum attempts for wallet deploy. Skipping")
                        current_deploy_failed_wallets.append(wallet_json)
                        current_deploy_failed_addresses.append(wallet.address)
                        write_to_json(DEPLOY_FAILED_WALLETS_JSON_PATH, current_deploy_failed_wallets)
                        break

                    logger.info(f"Running deploy for wallet {wallet.address}. Attempt {deploy_attempt}")
                    is_deployed = await deployer.deploy(
                        key_pair,
                        wallet.address,
                        should_skip_withdraw=deploy_attempt > 1
                    )
                    if not is_deployed:
                        current_deploy_failed_wallets.append(wallet_json)
                        write_to_json(DEPLOY_FAILED_WALLETS_JSON_PATH, current_deploy_failed_wallets)
                        break
                    else:
                        bar.next()
                        current_deploy_success_wallets.append(wallet.address)
                        current_deploy_success_wallets_json.append(wallet_json)
                        write_to_txt(DEPLOYED_WALLETS_TXT_PATH, [wallet.address])
                        write_to_json(DEPLOYED_WALLETS_JSON_PATH, current_deploy_success_wallets_json)
                        break
                except ClientError as e:
                    logger.error(
                        f"Starknet client error {e.message}. Sleeping for {CLIENT_ON_ERROR_SLEEP_IN_SEC}sec. Trying another attempt")
                except Exception as e:
                    logger.error(
                        f"Unexpected error {e}. Sleeping for {CLIENT_ON_ERROR_SLEEP_IN_SEC}sec. Trying another attempt"
                    )
                finally:
                    deploy_attempt = deploy_attempt + 1
                    time.sleep(CLIENT_ON_ERROR_SLEEP_IN_SEC)

            if index:
                deploy_sleep = DeployWallets.get_deploy_sleep_time()
                logger.info(f"Sleeping before next deploy for {deploy_sleep}sec.")
                time.sleep(deploy_sleep)

        logger.info(
            f"All wallets were attempted to deploy. Failed: {len(current_deploy_failed_wallets)}. Success: {len(current_deploy_success_wallets)}")

        if len(current_deploy_success_wallets) != 0:
            current_deploy_success_wallets.insert(0, str(datetime.now()))
            current_deploy_success_wallets.append("")

        # logger.info(f"Saving failed wallets to {DEPLOY_FAILED_WALLETS_JSON_PATH}")
        # write_to_json(DEPLOY_FAILED_WALLETS_JSON_PATH, current_deploy_failed_wallets)
        # logger.info(f"Saving success wallets to {DEPLOYED_WALLETS_TXT_PATH}")
        # write_to_txt(DEPLOYED_WALLETS_TXT_PATH, current_deploy_success_wallets)
        logger.info("Saving state to files ended")
