import asyncio
import inspect

from config import ENDLESS_MENU
from loguru import logger

from greeting import greeting_message
from modules.provider import get_module


async def run_option(methods: list):
    for method in methods:
        if callable(method):
            if inspect.iscoroutinefunction(method):
                await method()
            else:
                method()
        else:
            print(f"Object {method} is not callable")


async def startup():
    try:
        while True:
            greeting_message()
            module = input("Module: ")
            if not module.isdigit():
                logger.error("Wrong module format. It should be number")

            if module == "0":
                logger.info("Shutting down. Bye!")
            else:
                logger.info(f"Start module {module}")

            worker = get_module(module)
            if not worker:
                logger.error("Wrong module number")

            await run_option(worker)

            if not ENDLESS_MENU:
                exit()

    except Exception as e:
        logger.exception(e)


asyncio.run(startup())
