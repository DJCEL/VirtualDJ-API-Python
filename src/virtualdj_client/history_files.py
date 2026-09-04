#------------------------------------------------------------------------------------
# VirtualDJ History
#------------------------------------------------------------------------------------
import os
import platform

__version__ = '1.0.0'

class VirtualDJHistoryFile():
    TRACKLIST_FILENAME = "tracklist.txt"
    FILES_EXTENSION = ".m3u"

    def get_local_history_files(self):
        system = platform.system()
        if system == "Windows":
            local_appdata = os.getenv('LOCALAPPDATA')
            if local_appdata:
                 self.read_tracklist_file(local_appdata)

    def read_tracklist_file(self,local_appdata:str):
        history_path = os.path.join(local_appdata, 'History', self.TRACKLIST_FILENAME)
        if os.path.exists(history_path):
            with open(history_path,"r", encoding="utf-8") as file:
                for line in file:
                    print(line)
         

