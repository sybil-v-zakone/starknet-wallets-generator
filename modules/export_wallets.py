from loguru import logger

from config import \
    GENERATED_WALLETS_JSON_PATH, \
    GENERATED_WALLETS_EXCEL_PATH, \
    DEPLOY_FAILED_WALLETS_EXCEL_PATH, \
    DEPLOY_FAILED_WALLETS_JSON_PATH, \
    DEPLOYED_WALLETS_TXT_PATH, \
    DEPLOYED_WALLETS_EXCEL_PATH
from sdk.export_to_excel import export


class ExportWallets:
    @staticmethod
    def export():
        logger.info("Starting ArgentX exporter")
        logger.info("Exporting generated wallets to Excel")

        export(GENERATED_WALLETS_JSON_PATH, GENERATED_WALLETS_EXCEL_PATH)

        logger.info("Exporting deploy-failed wallets to Excel")
        export(DEPLOY_FAILED_WALLETS_JSON_PATH, DEPLOY_FAILED_WALLETS_EXCEL_PATH)

        logger.info("Exporting deploy-successfull wallets to Excel")
        export(DEPLOYED_WALLETS_TXT_PATH, DEPLOYED_WALLETS_EXCEL_PATH)
