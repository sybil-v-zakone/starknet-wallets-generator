import random

from aiohttp import ClientSession
from aiohttp_socks import ProxyConnector

from loguru import logger
from starknet_py.net.account.account import Account
from starknet_py.net.gateway_client import GatewayClient
from starknet_py.net.models.chains import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair

import config
from sdk.cex import okx_withdraw
from sdk.topup_waiter import check_account_balance, wait_for_topup
from sdk.gas import gas_delay

from sdk.argentx.deploy import ArgentDeploy
from sdk.braavos.deploy import BraavosDeploy



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

    async def _get_deploy_provider(self):
        if config.WALLET_APPLICATION not in ["argentx", "braavos"]:
            logger.error("Wrong WALLET_APPLICATION. Run exit()")
            exit()
        if config.WALLET_APPLICATION == "argentx":
            return ArgentDeploy
        if config.WALLET_APPLICATION == "braavos":
            return BraavosDeploy

    @prepare_deploy
    @gas_delay(gas_threshold=config.GAS_THRESHOLD, delay_range=config.GAS_DELAY_RANGE)
    async def deploy(self, key_pair: KeyPair, address):
        await self.log_ip()
        await check_account_balance(self.chain, self.client, address, key_pair)

        provider = await self._get_deploy_provider()
        result = await provider.wallet_deploy(
            key_pair=key_pair,
            address=address,
            chain=self.chain,
            client=self.client
        )

        await self._finalize_client()
        return result
