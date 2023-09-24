import random

from aiohttp import ClientSession
from aiohttp_socks import ProxyConnector

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
    def __init__(
            self,
            network: str = config.STARKNET_NETWORK,
            chain: StarknetChainId = config.STARKNET_CHAIN_ID,
            proxy: str = None
    ):
        self.network = network
        self.chain = chain
        self.proxy = proxy
        self.session = None
        self.client = self._get_client()

    def _get_client(self):
        if self.proxy:
            self.session = ClientSession(connector=ProxyConnector.from_url(f'http://{self.proxy}'))

        return GatewayClient(
            net=self.network,
            session=self.session
        )
    
    async def _finalize_client(self):
        if self.session:
            await self.session.close()

    async def log_ip(self):
        try:
            if self.session:
                response = await self.session.get('https://ifconfig.me/ip')
                parsed_response = await response.text()

                logger.info(f'Your ip: {parsed_response.strip()}')
        except Exception as e:
            logger.error(f'Error occured while getting IP: {str(e)}')

    @prepare_deploy
    @gas_delay(gas_threshold=config.GAS_THRESHOLD, delay_range=config.GAS_DELAY_RANGE)
    async def deploy(self, key_pair: KeyPair, address):
        await self.log_ip()
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
        
        result = None
        if await account_deployment_result.wait_for_acceptance():
            logger.success(f"Wallet {address} successfully deployed")
            result = account_deployment_result
        else:
            logger.error(f"Wallet {address} is failed to deploy")
            result = False

        await self._finalize_client()
        return result
