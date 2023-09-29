from loguru import logger
from starknet_py.net.account.account import Account
from starknet_py.net.models.chains import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair

from sdk.braavos.signature import deploy_account_braavos

import constants



class BraavosDeploy():
    @staticmethod
    async def wallet_deploy(
            key_pair: KeyPair,
            address,
            chain: StarknetChainId,
            client
        ):
        constructor_calldata = [
            constants.BRAAVOS_IMPLEMENTATION_CLASS_HASH,
            constants.BRAAVOS_SELECTOR_HASH,
            1,
            key_pair.public_key

        ]

        account_deployment_result = await deploy_account_braavos(
            address=int(address, 16),
            class_hash=constants.BRAAVOS_PROXY_CLASS_HASH,
            salt=key_pair.public_key,
            key_pair=key_pair,
            client=client,
            chain=chain,
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

        return result