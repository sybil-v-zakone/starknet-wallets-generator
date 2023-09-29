from web3 import Web3

from sdk.braavos.key_derivation import compute_p_keys, calculate_braavos_address


class BraavosWalletGenerator:
    def __init__(self):
        self.w3 = Web3()
        self.w3.eth.account.enable_unaudited_hdwallet_features()

    def get_wallet_data(self):
        (account, mnemonic) = self.w3.eth.account.create_with_mnemonic()

        stark_pair, public_key, private_key = compute_p_keys(mnemonic)

        address = calculate_braavos_address(public_key)

        return {
            "seed": mnemonic,
            "address": hex(address),
            "private_key": private_key,
            "public_key": public_key,
            "stark_pair": stark_pair
        }
