#------------------------------------------------------------------------------------
# VirtualDJ History
#------------------------------------------------------------------------------------
import os
import platform
from pathlib import Path

__version__ = '1.0.2'

class VirtualDJHistoryFiles():
    TRACKLIST_FILENAME = "tracklist.txt"
    OTHER_FILES_EXTENSION = ".m3u"
    #------------------------------------------------------------------------------------
    def get_local_history_files(self):
        vdj_home = self._get_virtualdj_home()
       
        if os.path.exists(vdj_home):
            history_folder = os.path.join(vdj_home, 'History')
            self._read_tracklist_file(history_folder)
    #------------------------------------------------------------------------------------
    @staticmethod
    def _get_virtualdj_home():
        vdj_home = ""
        system = platform.system()
        if system == "Windows":
            local_appdata = os.getenv('LOCALAPPDATA')
            if local_appdata:
                vdj_home = os.path.join(local_appdata,'VirtualDJ')
        elif system == "Darwin":
            # vdj_home_old = Path.home() / "Documents" / "VirtualDJ""
            vdj_home = Path.home() / "Library" / "Application Support" / "VirtualDJ"

        return vdj_home
    #------------------------------------------------------------------------------------
    def _read_tracklist_file(self, history_folder:str):
        history_path = os.path.join(history_folder, self.TRACKLIST_FILENAME)
        if os.path.exists(history_path):
            with open(history_path,"r", encoding="utf-8") as file:
                for line in file:
                    print(line)
         

