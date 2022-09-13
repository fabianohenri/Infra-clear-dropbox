import datetime
import logging
import os

from controller.dropbox_clean import DrobpoxController
from resources.object_storage import ObjectStorage
from utils.constants import Path
from utils.logging_format import LoggingFormat

if __name__ == '__main__':

    now = datetime.datetime.now()
    date_fmt = now.strftime("%d-%m-%Y")

    if not os.path.exists(Path.TMP_DIR):
        os.mkdir(Path.TMP_DIR)

    if not os.path.exists(Path.TMP_DIR + "/log"):
        os.mkdir(Path.TMP_DIR + "/log")

    log_name = Path.TMP_DIR + "/log/" + date_fmt + '.log'

    # Criar logger customizado
    logger = logging.getLogger("Dropbox Clear")

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(log_name)
    c_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.DEBUG)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    DrobpoxController.clear()

    # Enviando arquivo de log para o object storage
    ObjectStorage.upload()

    message = "Processo de limpeza terminado com sucesso."
    LoggingFormat.format(message, "Success")

