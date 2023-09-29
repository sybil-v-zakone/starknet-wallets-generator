import hashlib

from eth_account.hdaccount import (
    seed_from_mnemonic,
    key_from_seed
)
from starknet_py.hash.address import compute_address
from starknet_py.hash.selector import get_selector_from_name
from starknet_py.hash.utils import private_to_stark_key
from starknet_py.net.signer.stark_curve_signer import KeyPair

from constants import (
    BRAAVOS_PROXY_CLASS_HASH,
    BRAAVOS_IMPLEMENTATION_CLASS_HASH,
    BRAAVOS_EC_ORDER,
    BASE_DERIVATION_PATH
)


def eip_2645_hashing(key_0):
    N = 2 ** 256
    stark_curve_order = int(BRAAVOS_EC_ORDER)

    n_minus_n = N - (N % stark_curve_order)
    i = 0
    while True:
        x = key_0 + bytes([i])
        key_hash = int(hashlib.sha256(x).hexdigest(), 16)
        if key_hash < n_minus_n:
            return hex(key_hash % stark_curve_order)

        i += 1


def get_braavos_stark_pair(mnemonic, account_index):
    seed = seed_from_mnemonic(mnemonic, "")

    hdnode_private_key = key_from_seed(seed, BASE_DERIVATION_PATH)

    ground_key = eip_2645_hashing(hdnode_private_key)

    stark_pair = KeyPair.from_private_key(int(ground_key, 16))

    return stark_pair, ground_key


def compute_p_keys(mnemonic):
    stark_pair, ground_key = get_braavos_stark_pair(mnemonic, 5)
    public_key = private_to_stark_key(stark_pair.private_key)

    return stark_pair, hex(public_key), ground_key


def calculate_initializer(public_key):
    return int(public_key, 16)


def build_proxy_constructor(initializer):
    return [
        int(BRAAVOS_IMPLEMENTATION_CLASS_HASH),
        get_selector_from_name('initializer'),
        1,
        initializer
    ]


def build_proxy_constructor_call_data(public_key):
    initializer = calculate_initializer(public_key)
    return build_proxy_constructor(initializer)


def calculate_braavos_address(public_key):
    proxy_constructor_call_data = build_proxy_constructor_call_data(public_key)

    return compute_address(
        class_hash=int(BRAAVOS_PROXY_CLASS_HASH),
        constructor_calldata=proxy_constructor_call_data,
        salt=int(public_key, 16),
        deployer_address=0
    )
