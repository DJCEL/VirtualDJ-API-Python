#------------------------------------------------------------------------------------
# VirtualDJ - Folders structure
#------------------------------------------------------------------------------------

__version__ = '1.0.0'

import os
import platform
from pathlib import Path
from typing import Optional
import psutil
import subprocess
import logging

from .client_config import VDJ_CLIENT_DEBUG
from .client_config import VDJ_PROCESS_NAME, VDJ_PROCESS_PATH_WINDOWS, VDJ_PROCESS_PATH_MAC, VDJ_PROCESS_SETTINGS

logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------------------------------------------------------------
class VirtualDJClientUtils:
    def __init__(self):
        self.LOG_FOLDER = './log'
        self.LOG_FILENAME = 'client.log'

        self._CreateClientLog()
    #------------------------------------------------------------------------------------
    def _CreateClientLog(self):
        if VDJ_CLIENT_DEBUG:
            filepath = f"{self.LOG_FOLDER}/{self.LOG_FILENAME}"
            if not os.path.exists(self.LOG_FOLDER):
                os.makedirs(self.LOG_FOLDER)
            logging.basicConfig(filename=filepath, level=logging.INFO)
    #------------------------------------------------------------------------------------
    def SaveClientLog(self, msg):
        if VDJ_CLIENT_DEBUG:
            logger.info(msg)
    #------------------------------------------------------------------------------------
    def get_virtualdj_home(self) -> Optional[Path]:
        system = platform.system()
        if system == "Windows":
            # vdj_home_old = "C:\\Users\\<username>\\Documents\\VirtualDJ"
            local_appdata = os.getenv('LOCALAPPDATA')
            if not local_appdata:
                return None
            else:
                return os.path.join(local_appdata,'VirtualDJ')
        elif system == "Darwin":
            # vdj_home_old = Path.home() / "Documents" / "VirtualDJ"
            return Path.home() / "Library" / "Application Support" / "VirtualDJ"
        else:
            return None
    #------------------------------------------------------------------------------------
    def get_virtualdj_home_ext_list(self) -> list[Path]:
        vdj_home_ext_list : list[Path]= []
        system = platform.system()
        if system == "Windows":
            drives_Windows = self._windows_drive_roots()
            for drive in drives_Windows:
                vdj_home_ext = os.path.join(drive + "\\",'VirtualDJ')
                vdj_home_ext_list.append(vdj_home_ext)
        elif system == "Darwin":
            drives_Darwin = self._darwin_drive_roots()
            for drive in drives_Darwin:
                vdj_home_ext = os.path.join(drive, "VirtualDJ")
                vdj_home_ext_list.append(vdj_home_ext)

        return vdj_home_ext_list
    #------------------------------------------------------------------------------------
    @staticmethod
    def _windows_drive_roots() -> list[Path]:
        drives_Windows = [ chr(x) + ":" for x in range(65,91) if os.path.exists(chr(x) + ":") ]
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

        # TODO: check if updates are activated in VirtualDJ via settings.xml

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
            self.SaveClientLog(f"VirtualDJ not found: {app_path}")
            return False
        except Exception as e:
            msg =  app_path + "\n" + str(e)
            print(msg)
            self.SaveClientLog(msg)
            return False

        return True