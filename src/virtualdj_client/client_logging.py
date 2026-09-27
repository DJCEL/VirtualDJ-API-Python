#------------------------------------------------------------------------------------
# Logging
#------------------------------------------------------------------------------------
__version__ = '1.0.3'

import logging
from logging.handlers import RotatingFileHandler
from typing import Literal
import os
import sys

from .client_config import VDJ_CLIENT_DEBUG, VDJ_CLIENT_LOG_FOLDER, VDJ_CLIENT_LOG_FILENAME

#------------------------------------------------------------------------------------------------------------------------------------
class VdjClientLog:
    def __init__(self, controller = None, parent_name: str | None = None):
        self.filepath = f"{VDJ_CLIENT_LOG_FOLDER}/{VDJ_CLIENT_LOG_FILENAME}"
        if not os.path.exists(VDJ_CLIENT_LOG_FOLDER):
            os.makedirs(VDJ_CLIENT_LOG_FOLDER)

        self.logger = self.create_client_log(controller, parent_name, level="INFO", useRichHandler=True)
    #------------------------------------------------------------------------------------
    def create_client_log(self, controller, parent_name: str | None = None, level: Literal["DEBUG","INFO","WARNING","ERROR","CRITICAL"] = "INFO", useRichHandler: bool = False) -> logging.Logger | None:
        
        if parent_name is None:
            logger = logging.getLogger()
        else:
            logger = logging.getLogger(parent_name)


        logger.setLevel(logging.INFO)

        FORMAT = '%(asctime)s [%(name)s] %(message)s'
        formatter = logging.Formatter(FORMAT)

        try:
            file_handler = RotatingFileHandler(filename=self.filepath, mode="a", maxBytes=(1024*1024), backupCount=3, encoding='utf-8')
        except Exception as e:
            print("Failed to set up log file: %s" % str(e))
            return None
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        if useRichHandler:
            from rich.console import Console
            from rich.logging import RichHandler
            console_handler = RichHandler(console=Console(stderr=True), rich_tracebacks=True)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        else:
            console_log_output = sys.stdout
            console_handler = logging.StreamHandler(console_log_output)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)


        return logger
        #------------------------------------------------------------------------------------
    def get_client_log(self) -> logging.Logger:
        return self.logger
    #------------------------------------------------------------------------------------
    def save_client_log(self, msg: str, parent_name: str | None = None, level: Literal["DEBUG","INFO","WARNING","ERROR","CRITICAL"] = "INFO") -> None:
            if VDJ_CLIENT_DEBUG == False:
                return None


            if parent_name is None:
                logger = logging.getLogger()
            else:
                logger = logging.getLogger(parent_name)

            if level == "DEBUG":
                logger.debug(msg)
            elif level == "INFO":
                logger.info(msg)
            elif level == "WARNING":
                logger.warning(msg)
            elif level == "ERROR":
                logger.error(msg)
            elif level == "CRITICAL":
                logger.critical(msg)

    #------------------------------------------------------------------------------------
    def close_client_logs() -> None:
         self.logger.shutdown()
         logging.shutdown()