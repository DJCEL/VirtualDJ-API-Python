#------------------------------------------------------------------------------------
# VirtualDJ History
#------------------------------------------------------------------------------------
__version__ = '1.0.4'

from pathlib import Path

from .client_utils import VirtualDJUtils
from .client_config import VDJ_FOLDER_HISTORY, VDJ_TRACKLIST_FILENAME

#------------------------------------------------------------------------------------
class VirtualDJHistoryFiles():
    def __init__(self):
        self.vdj_utils = VirtualDJUtils()
        self.FOLDER_HISTORY = VDJ_FOLDER_HISTORY
        self.TRACKLIST_FILENAME = VDJ_TRACKLIST_FILENAME
        self.OTHER_FILES_EXTENSION = ".m3u"
    #------------------------------------------------------------------------------------
    def get_local_history_files(self):
        vdj_home_list = self.vdj_utils.get_virtualdj_home_list()
        for vdj_home in vdj_home_list:
                history_folder = vdj_home / self.FOLDER_HISTORY
                if history_folder.exists():
                    self._read_tracklist_file(history_folder)
    #------------------------------------------------------------------------------------
    def _read_tracklist_file(self, history_folder:Path):
        history_path = history_folder / self.TRACKLIST_FILENAME
        if history_path.exists():
            with open(history_path,"r", encoding="utf-8") as file:
                for line in file:
                    print(line)
         

