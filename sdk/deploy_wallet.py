from loguru import logger
from starknet_py.hash.selector import get_selector_from_name
from starknet_py.net.account.account import Account
from starknet_py.net.gateway_client import GatewayClient
from starknet_py.net.models.chains import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair

import config
import constants
from sdk.cex import okx_withdraw
from sdk.topup_waiter import check_account_balance, wait_for_topup


def prepare_deploy(func):
    async def wrapper(self, key_pair: KeyPair, address):
        if not config.SHOULD_WITHDRAW_FOR_DEPLOY:
            return await func(self, key_pair, address)

        withdraw_status = okx_withdraw(address, config.WITHDRAW_FOR_DEPLOY_ETH_AMOUNT)
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
    async def deploy(self, key_pair: KeyPair, address):
        await check_account_balance(self.chain, self.client, address, key_pair)

        calldata = [key_pair.public_key, 0]
        constructor_calldata = [
            constants.ACCOUNT_CLASS_HASH,
            get_selector_from_name("initialize"),
            len(calldata),
            *calldata,
        ]

        account_deployment_result = await Account.deploy_account(
            address=int(address, 16),
            class_hash=constants.PROXY_CLASS_HASH,
            salt=key_pair.public_key,
            key_pair=key_pair,
            client=self.client,
            chain=self.chain,
            constructor_calldata=constructor_calldata,
            auto_estimate=True,
        )

        logger.info(
            f"Sent a deploy tx for wallet {address} -> {constants.STARKSCAN_URL}/{account_deployment_result.hash}")
        if await account_deployment_result.wait_for_acceptance():
            logger.success(f"Wallet {address} successfully deployed")
            return account_deployment_result
        else:
            logger.error(f"Wallet {address} is failed to deploy")
            return False
