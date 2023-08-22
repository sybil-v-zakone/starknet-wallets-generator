from loguru import logger


def greeting_message():
    start_message = r'''        
                   __    _ __                        __                  
       _______  __/ /_  (_) /  _   __   ____  ____ _/ /______  ____  ___ 
      / ___/ / / / __ \/ / /  | | / /  /_  / / __ `/ //_/ __ \/ __ \/ _ \
     (__  ) /_/ / /_/ / / /   | |/ /    / /_/ /_/ / ,< / /_/ / / / /  __/   
    /____/\__, /_.___/_/_/    |___/    /___/\__,_/_/|_|\____/_/ /_/\___/ 
         /____/                                                          

    Modules:
    1: generate_wallets                                  | Generate ArgentX wallets
    2: deploy_wallets                                    | Deploy ArgentX wallets
    3: export_wallets                                    | Export ArgentX wallets from data-files to Excel files
    0: exit                                              | Exit
    '''
    logger.debug(start_message)
