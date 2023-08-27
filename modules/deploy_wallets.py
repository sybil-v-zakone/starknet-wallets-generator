import random
import time
from datetime import datetime

from loguru import logger
from progress.bar import IncrementalBar
from starknet_py.net.client_errors import ClientError
from starknet_py.net.signer.stark_curve_signer import KeyPair

from config import GENERATED_WALLETS_JSON_PATH, DEPLOY_FAILED_WALLETS_JSON_PATH, DEPLOYED_WALLETS_TXT_PATH, \
    DEPLOY_SLEEP_DEVIATION_IN_SEC, WITHDRAW_FOR_DEPLOY_ETH_AMOUNT, CEX_WITHDRAW_FEE, CLIENT_ON_ERROR_TOTAL_TRIES, \
    CLIENT_ON_ERROR_SLEEP_IN_SEC
from models.wallet import Wallet
from sdk.deploy_wallet import DeployWallet
from sdk.file import read_from_json, write_to_json, write_to_txt


class DeployWallets:
    @staticmethod
    def get_deploy_sleep_time():
        return random.randint(*DEPLOY_SLEEP_DEVIATION_IN_SEC)

    @staticmethod
    async def deploy():
        logger.info("Running deploy ArgentX wallets")
        deployer = DeployWallet()
        generated_wallets = read_from_json(GENERATED_WALLETS_JSON_PATH)
        previous_deploy_failed_wallets = read_from_json(DEPLOY_FAILED_WALLETS_JSON_PATH, True)

        current_deploy_failed_wallets = list()
        current_deploy_success_wallets = list()

        current_deploy_wallets = []
        if isinstance(generated_wallets, list):
            current_deploy_wallets.extend(generated_wallets)

        if isinstance(previous_deploy_failed_wallets, list):
            current_deploy_wallets.extend(previous_deploy_failed_wallets)

        logger.info(f"Total wallets for deploy: {len(current_deploy_wallets)}")
        logger.info(
            f"All wallets will be topup for {WITHDRAW_FOR_DEPLOY_ETH_AMOUNT}ETH. CEX fee is {CEX_WITHDRAW_FEE}ETH")
        bar = IncrementalBar('Deployed wallets', max=len(current_deploy_wallets))
        for index, wallet_json in enumerate(current_deploy_wallets, 1 - len(current_deploy_wallets)):
            wallet = Wallet(**wallet_json)
            key_pair = KeyPair.from_private_key(int(wallet.private_key, 16))

            deploy_attempt = 1
            while True:
                try:
                    if deploy_attempt > CLIENT_ON_ERROR_TOTAL_TRIES:
                        logger.info("Reached maximum attempts for wallet deploy. Skipping")
                        current_deploy_failed_wallets.append(wallet_json)
                        break

                    logger.info(f"Running deploy for wallet {wallet.address}. Attempt {deploy_attempt}")
                    is_deployed = await deployer.deploy(
                        key_pair,
                        wallet.address,
                        should_skip_withdraw=deploy_attempt > 1
                    )
                    if not is_deployed:
                        current_deploy_failed_wallets.append(wallet_json)
                        break
                    else:
                        bar.next()
                        current_deploy_success_wallets.append(wallet.address)
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

        logger.info(f"Saving failed wallets to {DEPLOY_FAILED_WALLETS_JSON_PATH}")
        write_to_json(DEPLOY_FAILED_WALLETS_JSON_PATH, current_deploy_failed_wallets)
        logger.info(f"Saving success wallets to {DEPLOYED_WALLETS_TXT_PATH}")
        write_to_txt(DEPLOYED_WALLETS_TXT_PATH, current_deploy_success_wallets)
        logger.info("Saving state to files ended")
