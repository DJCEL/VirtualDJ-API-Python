#------------------------------------------------------------------------------------
# VirtualDJ History
#------------------------------------------------------------------------------------
import os
from pathlib import Path
import platform

__version__ = '1.0.0'

class VirtualDJHistory():
    TRACKLIST_NAME = "tracklist.txt"

    def get_local_history_list(self) -> list[Path]:
        system = platform.system()

        if system == "Windows":
            local_appdata = os.getenv('LOCALAPPDATA')
            if local_appdata:
                history_path = os.path.join(local_appdata, 'History', self.TRACKLIST_NAME)
                if os.path.exists(history_path):
                        self.read_tracklist_file(history_path)

    def read_tracklist_file(filepath:str):
        with open(filepath,"r", encoding="utf-8") as file:
            for line in file:
                print(line)
         

