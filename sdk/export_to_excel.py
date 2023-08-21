import os
import pandas as pd
from loguru import logger

from sdk.file import read_from_json, read_from_txt

readers = {
    '.json': read_from_json,
    '.txt': read_from_txt
}


def export(file_to_read, file_to_save):
    file_extension = os.path.splitext(file_to_read)[1]
    reader = readers.get(file_extension)
    if not reader:
        logger.error(f"Current file to export({file_to_read}) extension is not supported. Supported extensions are .json and .txt")
        return False

    content = reader(file_to_read)
    df = pd.DataFrame(content)

    df.to_excel(file_to_save, index=False, engine='openpyxl')

    logger.info(f"Data exported to {file_to_save}")
