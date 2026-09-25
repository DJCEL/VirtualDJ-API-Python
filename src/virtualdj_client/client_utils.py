#------------------------------------------------------------------------------------
# VirtualDJ - Folders structure
#------------------------------------------------------------------------------------

__version__ = '1.0.3'

import os
import platform
from pathlib import Path
from typing import Optional, Literal
import psutil
import subprocess
import logging

from .client_config import VDJ_CLIENT_DEBUG, VDJ_PROCESS_NAME, VDJ_PROCESS_PATH_WINDOWS, VDJ_PROCESS_PATH_MAC

#------------------------------------------------------------------------------------------------------------------------------------
class VirtualDJUtils:
    def __init__(self):
        self.LOG_FOLDER = './log'
        self.LOG_FILENAME = 'client.log'
        self.logger = self.get_client_log(__name__)

        self._configure_client_log()
    #------------------------------------------------------------------------------------
    def _configure_client_log(self,level: Literal["DEBUG","INFO","WARNING,"ERROR","CRITICAL"] = "INFO") -> None:
        if VDJ_CLIENT_DEBUG:
            filepath = f"{self.LOG_FOLDER}/{self.LOG_FILENAME}"
            if not os.path.exists(self.LOG_FOLDER):
                os.makedirs(self.LOG_FOLDER)
            
            FORMAT = '%(asctime)s - %(message)s'
            handlers = list[logging.Handler] = []

            """
            file_handler = logging.FileHander(filename=filepath)
            file_handler.setLevel(level)
            formatter = logging.Formatter(FORMAT)
            file_handler.setFormatter(formatter)
            handlers.append(file_handler)
            """

            if not handlers:
               handlers.append(logging.StreamHandler())

            logging.basicConfig(filename=filepath, level=level, format=FORMAT)

#logging.basicConfig(level=level, format=FORMAT, handlers=handlers)
    #------------------------------------------------------------------------------------
    def get_client_log(self, name: str) -> logging.Logger:
        return logging.getLogger(str)
#------------------------------------------------------------------------------------
    def save_client_log(self, level: str = "INFO", msg: str):
        if VDJ_CLIENT_DEBUG:
            if level == "INFO":
                self.logger.info(msg)
    #------------------------------------------------------------------------------------
    def close_client_log(self):
        logging.shutdown()
    #------------------------------------------------------------------------------------
    def get_virtualdj_home_list(self) -> list[Path]:
        system = platform.system()
        if system == "Windows":
            main_folder_list = [ 
                Path.home() / "Documents",
            ]
            local_appdata = os.getenv('LOCALAPPDATA')
            if local_appdata:
               main_folder_list.append(Path(local_appdata))
        elif system == "Darwin":
            main_folder_list = [ 
                Path.home() / "Documents",
                Path.home() / "Library" / "Application Support",
            ]
        else:
            return []

        vdj_home_list: list[Path] = []
        for main_folder in main_folder_list:
            vdj_home = Path(main_folder) / "VirtualDJ"
            if vdj_home.exists():
                vdj_home_list.append(vdj_home)

        return vdj_home_list
    #------------------------------------------------------------------------------------
    def get_virtualdj_home_ext_list(self) -> list[Path]:
        system = platform.system()
        if system == "Windows":
            drives = self._windows_drive_roots()
        elif system == "Darwin":
            drives = self._darwin_drive_roots()
        else:
            return []
        
        vdj_home_ext_list: list[Path] = []
        for drive in drives:
            vdj_home_ext = Path(drive) / "VirtualDJ"
            if vdj_home_ext.exists():
                vdj_home_ext_list.append(vdj_home_ext)

        return vdj_home_ext_list
    #------------------------------------------------------------------------------------
    @staticmethod
    def _windows_drive_roots() -> list[Path]:
        drives_Windows = [ chr(x) + ":\\" for x in range(65,91) if os.path.exists(chr(x) + ":") ]
        return drives_Windows
    #------------------------------------------------------------------------------------
    @staticmethod
    def _darwin_drive_roots() -> list[Path]:
        volumes_path = Path("/Volumes")
        if not volumes_path.exists():
            return []
        drives_darwin = [volume for volume in volumes_path.iterdir() if volume.is_dir()]
        return drives_darwin
    #------------------------------------------------------------------------------------
    def is_virtualdj_running(self) -> bool:
        """ Check if VirtualDJ software is running """
        bRes = False
        for proc in psutil.process_iter(["pid", "name"]):
            process_name = proc.info["name"]
            if process_name and VDJ_PROCESS_NAME.lower() in process_name.lower():
                bRes = True

        return bRes
    #------------------------------------------------------------------------------------
    def launch_virtualdj_software(self) -> bool:
        """ Launch VirtualDJ software """
        system = platform.system()
        if system == "Windows":
            app_path = VDJ_PROCESS_PATH_WINDOWS
        elif system == "Darwin":
            app_path = os.path.join(VDJ_PROCESS_PATH_MAC,"Contents","MacOS","VirtualDJ")
        else:
            return False

        try:
            # Open the application in background:
            popen_kwargs = {
                 "stdin": subprocess.DEVNULL, 
                 "stdout": subprocess.DEVNULL,
                 "stderr": subprocess.DEVNULL,
                 "start_new_session": True
                }

            if system == "Windows":
                 popen_kwargs["creationflags"] = (subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS)

            subprocess.Popen([app_path], **popen_kwargs)
        except FileNotFoundError:
            print(f"VirtualDJ not found: {app_path}")
            self.save_client_log(f"VirtualDJ not found: {app_path}")
            return False
        except Exception as e:
            msg =  app_path + "\n" + str(e)
            print(msg)
            self.save_client_log(msg)
            return False

        return True