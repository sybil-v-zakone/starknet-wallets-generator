from progress.bar import Bar

import random
import time
from datetime import datetime

from loguru import logger
from starknet_py.net.signer.stark_curve_signer import KeyPair

from config import GENERATED_WALLETS_JSON_PATH, DEPLOY_FAILED_WALLETS_JSON_PATH, DEPLOYED_WALLETS_TXT_PATH, \
    DEPLOY_SLEEP_DEVIATION_IN_SEC, WITHDRAW_FOR_DEPLOY_ETH_AMOUNT, CEX_WITHDRAW_FEE
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
        previous_deploy_failed_wallets = read_from_json(DEPLOY_FAILED_WALLETS_JSON_PATH)

        current_deploy_failed_wallets = list()
        current_deploy_success_wallets = list()

        current_deploy_wallets = []
        if isinstance(generated_wallets, list):
            current_deploy_wallets.extend(generated_wallets)

        if isinstance(previous_deploy_failed_wallets, list):
            current_deploy_wallets.extend(previous_deploy_failed_wallets)

        logger.info(f"Total wallets for deploy: {len(current_deploy_wallets)}")
        logger.info(f"All wallets will be topup for {WITHDRAW_FOR_DEPLOY_ETH_AMOUNT}ETH. CEX fee is setted up to {CEX_WITHDRAW_FEE}ETH")
        bar = Bar('ChargingBar', max=len(current_deploy_wallets))
        for index, wallet_json in enumerate(current_deploy_wallets, 1 - len(current_deploy_wallets)):
            wallet = Wallet(**wallet_json)
            key_pair = KeyPair.from_private_key(int(wallet.private_key, 16))

            logger.info(f"Running deploy for wallet {wallet.address}")
            is_deployed = await deployer.deploy(key_pair, wallet.address)
            if not is_deployed:
                current_deploy_failed_wallets.append(wallet_json)
            else:
                bar.next()
                current_deploy_success_wallets.append(wallet.address)

            if index:
                deploy_sleep = DeployWallets.get_deploy_sleep_time()
                logger.info(f"Sleeping before next deploy for {deploy_sleep}sec.")
                time.sleep(deploy_sleep)

        if len(current_deploy_success_wallets) != 0:
            current_deploy_success_wallets.insert(0, str(datetime.now()))
            current_deploy_success_wallets.append("")

        logger.info(f"All wallets were attempted to deploy. Failed: {len(current_deploy_failed_wallets)}. Success: {len(current_deploy_success_wallets)}")
        logger.info(f"Saving failed wallets to {DEPLOY_FAILED_WALLETS_JSON_PATH}")
        write_to_json(DEPLOY_FAILED_WALLETS_JSON_PATH, current_deploy_failed_wallets)
        logger.info(f"Saving success wallets to {DEPLOYED_WALLETS_TXT_PATH}")
        write_to_txt(DEPLOYED_WALLETS_TXT_PATH, current_deploy_success_wallets)
        logger.info("Saving state to files ended")
