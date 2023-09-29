from loguru import logger
from progress.bar import IncrementalBar

from config import GENERATED_WALLETS_JSON_PATH, WALLETS_TO_GENERATE_COUNT, WALLET_APPLICATION
from models.wallet import Wallet
from sdk.argentx.wallet_generator import ArgentWalletGenerator
from sdk.braavos.wallet_generator import BraavosWalletGenerator
from sdk.file import write_to_json


class GenerateWallets:
    @staticmethod
    def generate():
        if WALLET_APPLICATION == "argentx":
            generator = ArgentWalletGenerator()
        if WALLET_APPLICATION == "braavos":
            generator = BraavosWalletGenerator()

        wallets = list()

        logger.info(f"Running {WALLET_APPLICATION} wallets generator")
        logger.info(f"Trying to generate {WALLETS_TO_GENERATE_COUNT} wallets")
        bar = IncrementalBar('Wallets generated:', max=WALLETS_TO_GENERATE_COUNT)
        for i in range(WALLETS_TO_GENERATE_COUNT):
            wallet = generator.get_wallet_data()
            wallet_model = Wallet(
                private_key=wallet["private_key"],
                address=wallet["address"],
                seed=wallet["seed"],
            )
            wallets.append(wallet_model.__dict__)
            bar.next()

        bar.finish()

        logger.info(f"Wallets are generated. Saving to {GENERATED_WALLETS_JSON_PATH}")
        write_to_json(GENERATED_WALLETS_JSON_PATH, wallets)
