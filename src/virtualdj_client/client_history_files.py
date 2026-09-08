#------------------------------------------------------------------------------------
# VirtualDJ History
#------------------------------------------------------------------------------------
__version__ = '1.0.3'

import os

from .client_utils import VirtualDJClientUtils
from .client_config import VDJ_FOLDER_HISTORY, VDJ_TRACKLIST_FILENAME

#------------------------------------------------------------------------------------
class VirtualDJHistoryFiles():
    def __init__(self):
        self.vdj_utils = VirtualDJClientUtils()
        self.FOLDER_HISTORY = VDJ_FOLDER_HISTORY
        self.TRACKLIST_FILENAME = VDJ_TRACKLIST_FILENAME
        self.OTHER_FILES_EXTENSION = ".m3u"
    #------------------------------------------------------------------------------------
    def get_local_history_files(self):
        vdj_home = self.vdj_utils.get_virtualdj_home()
        if vdj_home is not None:
            if os.path.exists(vdj_home):
                history_folder = os.path.join(vdj_home, self.FOLDER_HISTORY)
                self._read_tracklist_file(history_folder)
    #------------------------------------------------------------------------------------
    def _read_tracklist_file(self, history_folder:str):
        history_path = os.path.join(history_folder, self.TRACKLIST_FILENAME)
        if os.path.exists(history_path):
            with open(history_path,"r", encoding="utf-8") as file:
                for line in file:
                    print(line)
         

