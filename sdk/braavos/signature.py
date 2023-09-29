import dataclasses
from typing import List, Optional
from constants import BRAAVOS_CLASS_HASH

from starknet_py.net.client import Client
from starknet_py.hash.address import compute_address
from starknet_py.net.client_models import EstimatedFee
from starknet_py.net.signer.stark_curve_signer import KeyPair
from starknet_py.hash.utils import message_signature, compute_hash_on_elements
from starknet_py.net.account.account_deployment_result import AccountDeploymentResult
from starknet_py.net.models import AddressRepresentation, StarknetChainId, parse_address
from starknet_py.net.account.account import Account, _add_signature_to_transaction, _add_max_fee_to_transaction
from starknet_py.net.models.transaction import (
    DeployAccount,
    compute_deploy_account_transaction_hash,    
    AccountTransaction
)


async def sign_for_fee_estimate_braavos(
        provider, transaction
):
    version = transaction.version + 2 ** 128
    transaction = dataclasses.replace(transaction, version=version)
    signature = await sign_transaction_braavos(transaction, provider.signer.private_key)
    return _add_signature_to_transaction(tx=transaction, signature=signature)


async def _estimate_fee_braavos(provider, tx: AccountTransaction, block_hash=None, block_number=None):
    """
    :param tx: Transaction which fee we want to calculate.
    :param block_hash: a block hash.
    :param block_number: a block number.
    :return: Estimated fee.
    """
    tx = await sign_for_fee_estimate_braavos(provider, tx)
    estimated_fee = await provider._client.estimate_fee(
        tx=tx,
        block_hash=block_hash,
        block_number=block_number,
    )
    assert isinstance(estimated_fee, EstimatedFee)
    return estimated_fee


async def _get_max_fee_braavos_deploy(provider: Account, transaction, max_fee, auto_estimate):
    if auto_estimate and max_fee is not None:
        raise ValueError(
            "Arguments max_fee and auto_estimate are mutually exclusive."
        )

    if auto_estimate:
        estimated_fee = await _estimate_fee_braavos(provider, transaction)
        max_fee = int(estimated_fee.overall_fee * Account.ESTIMATED_FEE_MULTIPLIER)

    if max_fee is None:
        raise ValueError(
            "Argument max_fee must be specified when invoking a transaction."
        )
    return max_fee


async def deploy_account_braavos(
        *,
        address: AddressRepresentation,
        class_hash: int,
        salt: int,
        key_pair: KeyPair,
        client: Client,
        chain: StarknetChainId,
        constructor_calldata: Optional[List[int]] = None,
        nonce: int = 0,
        max_fee: Optional[int] = None,
        auto_estimate: bool = False,
) -> AccountDeploymentResult:
    """
    Deploys an account contract with provided class_hash on Starknet and returns
    an AccountDeploymentResult that allows waiting for transaction acceptance.
    Provided address must be first prefunded with enough tokens, otherwise the method will fail.
    If using Client for either TESTNET, TESTNET2 or MAINNET, this method will verify if the address balance
    is high enough to cover deployment costs.
    :param address: calculated and prefunded address of the new account.
    :param class_hash: class_hash of the account contract to be deployed.
    :param salt: salt used to calculate the address.
    :param key_pair: KeyPair used to calculate address and sign deploy account transaction.
    :param client: a Client instance used for deployment.
    :param chain: id of the Starknet chain used.
    :param constructor_calldata: optional calldata to account contract constructor. If ``None`` is passed,
        ``[key_pair.public_key]`` will be used as calldata.
    :param nonce: Nonce of the transaction.
    :param max_fee: max fee to be paid for deployment, must be less or equal to the amount of tokens prefunded.
    :param auto_estimate: Use automatic fee estimation, not recommend as it may lead to high costs.
    """

    address = parse_address(address)
    calldata = (
        constructor_calldata
        if constructor_calldata is not None
        else [key_pair.public_key]
    )
    if address != (
            computed := compute_address(
                salt=salt,
                class_hash=class_hash,
                constructor_calldata=calldata,
                deployer_address=0,
            )
    ):
        raise ValueError(
            f"Provided address {hex(address)} is different than computed address {hex(computed)} "
            f"for the given class_hash and salt."
        )

    account = Account(
        address=address, client=client, key_pair=key_pair, chain=chain
    )
    deploy_account_tx = await sign_deploy_account_transaction_braavos(
        class_hash=class_hash,
        contract_address_salt=salt,
        constructor_calldata=calldata,
        nonce=nonce,
        max_fee=max_fee,
        auto_estimate=auto_estimate,
        signer=account
    )
    if chain in (
            StarknetChainId.TESTNET,
            StarknetChainId.TESTNET2,
            StarknetChainId.MAINNET,
    ):
        balance = await account.get_balance()
        if balance < deploy_account_tx.max_fee:
            raise ValueError(
                "Not enough tokens at the specified address to cover deployment costs."
            )

    result = await client.deploy_account(deploy_account_tx)

    return AccountDeploymentResult(
        hash=result.transaction_hash, account=account, _client=account.client
    )


async def sign_deploy_account_transaction_braavos(
        class_hash: int,
        contract_address_salt: int,
        constructor_calldata: Optional[List[int]] = None,
        *,
        nonce: int = 0,
        max_fee: Optional[int] = None,
        auto_estimate: bool = False,
        signer: Account
) -> DeployAccount:
    constructor_calldata = constructor_calldata or []

    deploy_account_tx = DeployAccount(
        class_hash=class_hash,
        contract_address_salt=contract_address_salt,
        constructor_calldata=constructor_calldata,
        version=1,
        max_fee=0,
        signature=[],
        nonce=nonce,
    )
    max_fee = await _get_max_fee_braavos_deploy(
        provider=signer, transaction=deploy_account_tx, max_fee=max_fee, auto_estimate=auto_estimate
    )
    deploy_account_tx = _add_max_fee_to_transaction(deploy_account_tx, max_fee)
    signature = await sign_transaction_braavos(deploy_account_tx, signer.signer.private_key)
    return _add_signature_to_transaction(deploy_account_tx, signature)


async def _sign_deploy_account_transaction_braavos(transaction: DeployAccount, private_key: int):
    contract_address = compute_address(
        salt=transaction.contract_address_salt,
        class_hash=transaction.class_hash,
        constructor_calldata=transaction.constructor_calldata,
        deployer_address=0,
    )

    tx_hash = compute_deploy_account_transaction_hash(
        contract_address=contract_address,
        class_hash=transaction.class_hash,
        constructor_calldata=transaction.constructor_calldata,
        salt=transaction.contract_address_salt,
        max_fee=transaction.max_fee,
        version=transaction.version,
        chain_id=StarknetChainId.MAINNET,
        nonce=transaction.nonce,
    )

    tx_hash = compute_hash_on_elements([tx_hash, BRAAVOS_CLASS_HASH, 0, 0, 0, 0, 0, 0, 0])

    r, s = message_signature(msg_hash=tx_hash, priv_key=private_key)
    return [r, s, BRAAVOS_CLASS_HASH, 0, 0, 0, 0, 0, 0, 0]


async def sign_transaction_braavos(
        transaction: AccountTransaction, private_key: int
):
    if isinstance(transaction, DeployAccount):
        return await _sign_deploy_account_transaction_braavos(transaction, private_key)