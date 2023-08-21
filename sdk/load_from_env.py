import os
from dotenv import load_dotenv


def load():
    load_dotenv()

    env_dict = {}
    for key in os.environ:
        env_dict[key] = os.getenv(key)

    return env_dict
