import os
import pandas as pd
from loguru import logger

from sdk.file import read_from_json, read_from_txt

readers = {
    '.json': read_from_json,
    '.txt': read_from_txt
}


def get_reader(file_name):
    file_extension = os.path.splitext(file_name)[1]
    reader = readers.get(file_extension)
    if not reader:
        logger.error(
            f"Current file to export({file_name}) extension is not supported. Supported extensions are .json and .txt")
        return False
    return reader


def export_to_multiple_sheets(sheets: dict, file_to_save):
    try:
        logger.info(f"Exporting wallets data to {file_to_save}")

        with pd.ExcelWriter(file_to_save, engine='openpyxl') as writer:
            for sheet_name, file_to_read in sheets.items():
                reader = get_reader(file_to_read)
                if not reader:
                    continue

                content = reader(file_to_read)
                df = pd.DataFrame(content)
                df.to_excel(writer, sheet_name=sheet_name, index=False, engine='openpyxl')

        logger.info(f"Wallets data successfully exported to {file_to_save}")
    except Exception as e:
        logger.error(f"Failed to export wallets data -> {e}")


def export_to_one_sheet(file_to_read, file_to_save):
    reader = get_reader(file_to_read)
    if not reader:
        return False

    content = reader(file_to_read)
    df = pd.DataFrame(content)

    df.to_excel(file_to_save, index=False, engine='openpyxl')

    logger.info(f"Data exported to {file_to_save}")
