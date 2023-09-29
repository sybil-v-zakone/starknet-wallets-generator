from web3 import Web3

from sdk.argentx.key_derivation import get_stark_pair, calculate_argent_address


class ArgentWalletGenerator:
    def __init__(self):
        self.w3 = Web3()
        self.w3.eth.account.enable_unaudited_hdwallet_features()

    def get_wallet_data(self):
        (account, mnemonic) = self.w3.eth.account.create_with_mnemonic()

        stark_pair = get_stark_pair(account.key.hex())

        public_key = hex(stark_pair.public_key)
        private_key = hex(stark_pair.private_key)

        address = calculate_argent_address(public_key)

        return {
            "seed": mnemonic,
            "address": hex(address),
            "private_key": private_key,
            "public_key": public_key,
            "stark_pair": stark_pair
        }
