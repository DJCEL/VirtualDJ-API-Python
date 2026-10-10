#------------------------------------------------------------------------------------
# Logging
#------------------------------------------------------------------------------------
__version__ = '1.0.4'

import logging
from logging.handlers import RotatingFileHandler
from typing import Literal
import os
import sys

from .client_config import VDJ_CLIENT_DEBUG, VDJ_CLIENT_LOG_FOLDER, VDJ_CLIENT_LOG_FILENAME

#------------------------------------------------------------------------------------------------------------------------------------
class VdjClientLog:
    def __init__(self, controller = None, parent_name: str | None = None, useRichConsole: bool = False):
        self.filepath = f"{VDJ_CLIENT_LOG_FOLDER}/{VDJ_CLIENT_LOG_FILENAME}"
        if not os.path.exists(VDJ_CLIENT_LOG_FOLDER):
            os.makedirs(VDJ_CLIENT_LOG_FOLDER)

        self.logger = self.create_client_log(controller, parent_name, useRichConsole)
    #------------------------------------------------------------------------------------
    def create_client_log(self, controller, parent_name: str | None = None, useRichConsole: bool = False) -> logging.Logger | None:
        
        if parent_name is None:
            logger = logging.getLogger()
        else:
            logger = logging.getLogger(parent_name)

        logger.setLevel(logging.INFO)

        # do not propagate messages to the root logger
        logger.propagate = False

        # do not add handlers multiple times
        if logger.handlers:
            # we remove all the handlers
            #self._remove_handlers(logger)
            return logger

        # We create the handlers: file + console
        # %(filename)s - %(lineno)d - %(funcName)s
        FORMAT = '%(asctime)s - %(levelname)s - [%(name)s] %(message)s'
        formatter = logging.Formatter(FORMAT,datefmt="%Y/%m/%d %H:%M:%S")

        try:
            #maxBytes=(1024*1024)
            file_handler = RotatingFileHandler(filename=self.filepath, mode="a", maxBytes=0, backupCount=3, encoding='utf-8')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            print("Failed to set up log file: %s" % str(e))
            return None
        
        if useRichConsole:
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
    def _remove_handlers(self):
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)
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
                logger.debug(msg=msg)
            elif level == "INFO":
                try:
                    logger.info(msg=msg)
                except Exception as e:
                    print(f"Failed to log message: {msg}. Error: {str(e)}")
            elif level == "WARNING":
                logger.warning(msg=msg)
            elif level == "ERROR":
                logger.error(msg=msg)
            elif level == "CRITICAL":
                logger.critical(msg=msg)
            

    #------------------------------------------------------------------------------------
    def close_client_logs() -> None:
         self.logger.shutdown()
         logging.shutdown()