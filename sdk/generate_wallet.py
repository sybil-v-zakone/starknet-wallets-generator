from web3 import Web3

from sdk.key_derivation import get_stark_pair, build_constructor_calldata, calculate_argent_address


class GenerateWallet:
    def __init__(self):
        self.w3 = Web3()
        self.w3.eth.account.enable_unaudited_hdwallet_features()

    def get_wallet_data(self):
        (account, mnemonic) = self.w3.eth.account.create_with_mnemonic()

        stark_pair = get_stark_pair(account.key.hex())

        public_key = hex(stark_pair.public_key)
        private_key = hex(stark_pair.private_key)

        constructor_call_data = build_constructor_calldata(public_key)
        address = calculate_argent_address(public_key, constructor_call_data)

        return {
            "seed": mnemonic,
            "address": hex(address),
            "private_key": private_key,
            "public_key": public_key,
            "stark_pair": stark_pair
        }
