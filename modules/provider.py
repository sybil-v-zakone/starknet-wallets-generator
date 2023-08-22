from modules.deploy_wallets import DeployWallets
from modules.export_wallets import ExportWallets
from modules.generate_wallets import GenerateWallets

modules_map = {
    "0": [exit],
    "1": [GenerateWallets.generate],
    "2": [DeployWallets.deploy],
    "3": [ExportWallets.export]
}


def get_module(number):
    return modules_map.get(number)
