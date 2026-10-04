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
import sqlite3
from contextlib import closing

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
        system = platform.system().lower()
        if system == "windows":
            drives = self._windows_drive_roots()
        elif system == "darwin":
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
        #drives_windows = []
        #letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        #for letter in letters:
        #    root = Path(f"{letter}:/")
        #    if root.exists():
        #        drives_windows.append(root)
        drives_windows = [ chr(x) + ":\\" for x in range(65,91) if os.path.exists(chr(x) + ":") ]
        return drives_windows
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
        system = platform.system().lower()
        if system == "windows":
        
            for proc in psutil.process_iter(["pid", "name"]):
                process_name = proc.info["name"]
                if process_name and VDJ_PROCESS_NAME.lower() in process_name.lower():
                    bRes = True
        elif system == "darwin":
            script = 'tell application "System Events" to return exists process "VirtualDJ"'
            r = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True,
               text=True,
               timeout=15,
            )
            bRes = (r.stdout.strip().lower() ==  "true")

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
            self.vdj_client_log.save_client_log(msg=f"VirtualDJ not found: {app_path}",parent_name=__name__, level="ERROR")
            return False
        except Exception as e:
            msg =  app_path + "\n" + str(e)
            self.vdj_client_log.save_client_log(msg=msg,parent_name=__name__, level="ERROR")
            return False

        return True
    #------------------------------------------------------------------------------------
    def sqlite_query(self, database_path: Path, sql_script) -> list[dict]:
        result = []
        try:
           with sqlite3.connect(database_path, timeout=3) as connection:
               connection.row_factory = sqlite3.Row
               with closing(connection.cursor()) as cursor:
                    rows = cursor.execute(sql_script).fetchall()
                    for row in rows:
                        value = dict(row)
                        result.append(value)
        except Exception as e:
            message = str(e)
            strMsgLog = f"Failed to query the sqlite database: {message}"
            self.vdj_client_log.save_client_log(msg=strMsgLog, parent_name=__name__, level="ERROR")
            result = []

        return result