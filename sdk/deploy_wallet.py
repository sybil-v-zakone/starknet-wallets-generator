import random

from loguru import logger
from starknet_py.net.account.account import Account
from starknet_py.net.gateway_client import GatewayClient
from starknet_py.net.models.chains import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair

import config
import constants
from sdk.cex import okx_withdraw
from sdk.topup_waiter import check_account_balance, wait_for_topup
from sdk.gas import gas_delay


def prepare_deploy(func):
    async def wrapper(self, key_pair: KeyPair, address, should_skip_withdraw = True):
        if not config.SHOULD_WITHDRAW_FOR_DEPLOY or should_skip_withdraw:
            return await func(self, key_pair, address)

        withdraw_amount = random.uniform(*config.WITHDRAW_FOR_DEPLOY_ETH_AMOUNT)
        withdraw_status = okx_withdraw(address, withdraw_amount)
        if not withdraw_status:
            return False
        initial_balance = await check_account_balance(self.chain, self.client, address, key_pair)
        status = await wait_for_topup(initial_balance, self.chain, self.client, address, key_pair)
        if status:
            result = await func(self, key_pair, address)
            return result
        else:
            return False

    return wrapper


class DeployWallet:
    def __init__(self, network: str = config.STARKNET_NETWORK, chain: StarknetChainId = config.STARKNET_CHAIN_ID):
        self.network = network
        self.chain = chain
        self.client = GatewayClient(net=network)

    @prepare_deploy
    @gas_delay(gas_threshold=config.GAS_THRESHOLD, delay_range=config.GAS_DELAY_RANGE)
    async def deploy(self, key_pair: KeyPair, address):
        await check_account_balance(self.chain, self.client, address, key_pair)

        constructor_calldata = [
            key_pair.public_key,
            0
        ]

        account_deployment_result = await Account.deploy_account(
            address=int(address, 16),
            class_hash=constants.ACCOUNT_CLASS_HASH,
            salt=key_pair.public_key,
            key_pair=key_pair,
            client=self.client,
            chain=self.chain,
            constructor_calldata=constructor_calldata,
            auto_estimate=True
        )

        logger.info(
            f"{constants.STARKSCAN_URL}/{hex(account_deployment_result.hash)}")
        if await account_deployment_result.wait_for_acceptance():
            logger.success(f"Wallet {address} successfully deployed")
            return account_deployment_result
        else:
            logger.error(f"Wallet {address} is failed to deploy")
            return False
