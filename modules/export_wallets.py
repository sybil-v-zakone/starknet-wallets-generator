from loguru import logger

from config import WALLETS_EXCEL_PATH
from constants import WALLET_EXPORT_SHEETS
from sdk.export_to_excel import export_to_multiple_sheets


class ExportWallets:
    @staticmethod
    def export():
        logger.info("Starting ArgentX exporter")
        export_to_multiple_sheets(WALLET_EXPORT_SHEETS, WALLETS_EXCEL_PATH)
