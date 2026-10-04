#------------------------------------------------------------------------------------
# VirtualDJ - Folders structure
#------------------------------------------------------------------------------------

__version__ = '1.0.4'

import os
import platform
from pathlib import Path
from typing import Optional, Literal
import psutil
import subprocess
import logging

from .client_config import VDJ_PROCESS_NAME, VDJ_PROCESS_PATH_WINDOWS, VDJ_PROCESS_PATH_MAC
from .client_logging import VdjClientLog

#------------------------------------------------------------------------------------------------------------------------------------
class VirtualDJUtils:
    def __init__(self, controller = None):
        self.vdj_client_log = VdjClientLog(controller,__name__)
        self.VIRTUALDJ_FOLDER = "VirtualDJ"
    #------------------------------------------------------------------------------------
    def get_virtualdj_home_list(self) -> list[Path]:
        system = platform.system().lower()
        home = Path.home()
        if system == "windows":
            main_folder_list = [ 
                home / "Documents",
                home / "OneDrive" / "Documents",
            ]
            #userprofile = os.environ.get("USERPROFILE")
            localappdata = os.getenv('LOCALAPPDATA')
            if localappdata:
               main_folder_list.append(Path(localappdata))
        elif system == "darwin":
            main_folder_list = [ 
                home / "Documents",
                home / "Library" / "Application Support",
            ]
        else:
            return []

        vdj_home_list: list[Path] = []
        for main_folder in main_folder_list:
            vdj_home = Path(main_folder) / self.VIRTUALDJ_FOLDER
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
            vdj_home_ext = Path(drive) / self.VIRTUALDJ_FOLDER
            if vdj_home_ext.exists():
                vdj_home_ext_list.append(vdj_home_ext)

        return vdj_home_ext_list
    #------------------------------------------------------------------------------------
    @staticmethod
    def _windows_drive_roots() -> list[Path]:
        #letters_list="DEFGHIJKLMNOPQRSTUVWXYZ"
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
            self.vdj_client_log.save_client_log(f"VirtualDJ not found: {app_path}",__name__)
            return False
        except Exception as e:
            msg =  app_path + "\n" + str(e)
            self.vdj_client_log.save_client_log(msg,__name__)
            return False

        return True