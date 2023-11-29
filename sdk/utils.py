import requests
from config import USE_MOBILE_PROXY, IP_CHANGE_LINK
from loguru import logger



def change_mobile_ip() -> None:
    try:
        if USE_MOBILE_PROXY:
            res = requests.get(IP_CHANGE_LINK)

            if res.status_code == 200:
                logger.info("IP address changed successfully", send_to_tg=False)
            else:
                raise Exception("Failed to change IP address")

    except Exception as e:
        raise Exception(f"Encountered an error when changing ip address, check your proxy provider: {e}")