import logging


class LoggingFormat:

    @staticmethod
    def format(message: str, color: str):
        logger = logging.getLogger("Dropbox Clear")
        logging.disable(10)
        logger.setLevel(20)
        if not message:
            logger.info('\033[33m' + "Messangem não enviada para o logging" + "\033[0;0m")
        if not color:
            logger.info("\033[37m" + message + "\033[0;0m")
        if "Error" in color:
            # Cor Vermelha
            logger.warning("\033[1;31m" + message + "\033[0;0m")
        elif "Info" in color:
            # Cor branca
            logger.info("\033[97m" + message + "\033[0;0m")
        elif "Success" in color:
            # Cor verde
            logger.info("\033[1;32m" + message + "\033[0;0m")
        elif "Alert" in color:
            # Cor Amarela
            logger.info("\033[33m" + message + "\033[0;0m")
