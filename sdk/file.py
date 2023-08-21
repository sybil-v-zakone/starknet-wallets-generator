import json

from loguru import logger


def read_from_txt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            return [line.strip() for line in file]
    except FileNotFoundError as e:
        logger.error(f"{str(e)} while try to open \"{file_path}\"")
    except Exception as e:
        logger.error(f"{str(e)} while open txt file: \"{file_path}\"")


def write_to_txt(file_path, lines: list):
    try:
        with open(file_path, 'a') as file:
            for line in lines:
                file.write("%s\n" % line)
    except FileNotFoundError as e:
        logger.error(f"{str(e)} while try to open \"{file_path}\"")
    except Exception as e:
        logger.error(f"{str(e)} while write to txt file: \"{file_path}\"")


def read_from_json(file_path):
    try:
        with open(file_path) as json_file:
            return json.load(json_file)
    except FileNotFoundError as e:
        logger.error(f"{str(e)} while try to open \"{file_path}\"")
    except Exception as e:
        logger.error(f"{str(e)} while open json file: \"{file_path}\"")


def write_to_json(file_path, data):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
