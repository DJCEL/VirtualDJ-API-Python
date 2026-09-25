import logging
from typing import Literal

from .client_config import VDJ_CLIENT_DEBUG

LOG_FOLDER = './log'
LOG_FILENAME = 'client.log'

def configure_client_log(level: Literal["DEBUG","INFO","WARNING","ERROR","CRITICAL"] = "INFO") -> None:
            filepath = f"{LOG_FOLDER}/{LOG_FILENAME}"
            if not os.path.exists(LOG_FOLDER):
                os.makedirs(LOG_FOLDER)
            
            FORMAT = '%(asctime)s - %(message)s'
            handlers = list[logging.Handler] = []
            
            file_handler = logging.FileHander(filename=filepath)
            file_handler.setLevel(level)
            formatter = logging.Formatter(FORMAT)
            file_handler.setFormatter(formatter)
            handlers.append(file_handler)
            
            if not handlers:
               handlers.append(logging.StreamHandler())

            logging.basicConfig(filename=filepath, level=level, format=FORMAT)

            #logging.basicConfig(level=level, format=FORMAT, handlers=handlers)
#------------------------------------------------------------------------------------
def get_client_log(name: str) -> logging.Logger:
        return logging.getLogger(str)
#------------------------------------------------------------------------------------
def save_client_log(msg: str, level: str = "INFO", name: str = "__name__") -> None:
        if VDJ_CLIENT_DEBUG == False:
            return

        logger = get_client_log(name)

        if level == "INFO":
            logger.info(msg)
#------------------------------------------------------------------------------------
def close_client_log():
        logging.shutdown()