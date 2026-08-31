 
import os
import platform
import xml.etree.ElementTree as ET
from typing import Literal, TypedDict

__version__ = '1.0.5'
 
 
class VirtualDJSongsDatabase:
    #------------------------------------------------------------------------------------
    # VirtualDJ databases
    #------------------------------------------------------------------------------------
    class VDJPoiType:
        name : Literal['automix','beatgrid','remix']
    #------------------------------------------------------------------------------------
    class VDJPoiPoint:
        name : Literal['realStart','realEnd','fadeStart','fadeEnd','cutStart','cutEnd','tempoStart','tempoEnd']
    #------------------------------------------------------------------------------------
    class VdjPoi(TypedDict):
        Name: str
        Pos: float
        Type: str
        Point: str
        Num: int
        Bpm: float
        Phrase: int
        Size: float
        Slot: int
   #------------------------------------------------------------------------------------
    class VdjSong():
       FilePath: str
       FileSize: int
       Flag: int
       Tags_Author: str
       Tags_Title: str
       Tags_Year: int
       Tags_Genre: str
       Tags_Bpm: float
       Tags_Key: str
       Tags_Album: str
       Tags_Composer: str
       Tags_Label: str
       Tags_TrackNumber: str
       Tags_Remix: str
       Tags_Stars: int
       Tags_Remixer: str
       Tags_Grouping: str
       Tags_User1: str
       Tags_User2: str
       Tags_Internal: str
       Tags_Flag: int
       Infos_SongLength: float
       Infos_LastModified: int
       Infos_FirstSeen: int
       Infos_FirstPlay: int
       Infos_LastPlay: int
       Infos_PlayCount: int
       Infos_Bitrate: int
       Infos_Cover: int
       Infos_Color: int
       Infos_Corrupted: int
       Infos_Gain: int
       Infos_UserColor: str
       Comment: str
       Scan_Version: int
       Scan_Bpm: float
       Scan_Phase: float
       Scan_AltBpm: float
       Scan_Rigid: float
       Scan_Volume: float
       Scan_Key: str
       Scan_AudioSig: str
       Scan_Flag: int
       Scan_Beatgrid: list[str]
       Poi: list[VdjPoi]
       CustomMix: str
       Link_NetSearch: str
       Link_Cover: str
       Link_clouddriveId: str
    #------------------------------------------------------------------------------------
    def get_local_database_list(self):
        database_list = []
        xml_database_name = "database.xml"
        sqlite1_database_name = "extra.db"
        sqlite2_database_name = "cache.db"

        # sqlite1_tables_name = ["lyrics","related_tracks","track_data"]
        # sqlite2_tables_name = ["waveforms"]

        system = platform.system()

        if system == "Windows":
            appData_Local = os.getenv('LOCALAPPDATA')
            if appData_Local:
                main_XMLdatabase_path = os.path.join(appData_Local, 'VirtualDJ', xml_database_name)
                if os.path.exists(main_XMLdatabase_path):
                    database_list.append(main_XMLdatabase_path)
                main_SQLite1database_path = os.path.join(appData_Local,'VirtualDJ', sqlite1_database_name)
                if os.path.exists(main_SQLite1database_path):
                    database_list.append(main_SQLite1database_path)
                main_SQLite2database_path = os.path.join(appData_Local,'VirtualDJ', 'Cache', sqlite2_database_name)
                if os.path.exists(main_SQLite2database_path):
                    database_list.append(main_SQLite2database_path)

            drives_Windows = [ chr(x) + ":" for x in range(65,91) if os.path.exists(chr(x) + ":") ]

            for drive in drives_Windows:
                drive_full = drive + "\\"
                external_XMLdatabase_path = os.path.join(drive_full,'VirtualDJ', xml_database_name)
                if os.path.exists(external_XMLdatabase_path):
                    database_list.append(external_XMLdatabase_path)
                external_SQLite1database_path = os.path.join(drive_full,'VirtualDJ', sqlite1_database_name)
                if os.path.exists(external_SQLite1database_path):
                    database_list.append(external_SQLite1database_path)
                external_SQLite2database_path = os.path.join(drive_full,'VirtualDJ', 'Cache', sqlite2_database_name)
                if os.path.exists(external_SQLite2database_path):
                    database_list.append(external_SQLite2database_path)

            database_list_noduplicates = list(dict.fromkeys(database_list))

            return database_list_noduplicates

        elif system == "Darwin":
            #TODO: list of drives
            return database_list

        return database_list
    #------------------------------------------------------------------------------------
    def read_local_XMLdatabase(self, database_path: str, readAllSongs: bool = False):
        tree = ET.parse(database_path)
        root = tree.getroot()
        root_tag = root.tag
        id = 0
        songs_count = 0

        xmlTag_Song = ["Song"]
        xmlTag_Song_Data = ["Tags","Infos","Scan","CustomMix","Link"]
        xmlTag_Song_Poi = ["Poi"]
        xmlTag_Song_Comment = ["Comment"]


        if root_tag == "VirtualDJ_Database":
            root_attrib = root.attrib
            print(f"VirtualDJ database reading => {root_attrib}")
            songs_count = len(root.findall(".//" +  xmlTag_Song[0]))
            print(f"VirtualDJ database reading => Number of songs found = {songs_count}")
            if readAllSongs:
                for child in root:
                    child_tag = child.tag
                    if child_tag in xmlTag_Song:
                        i = 0
                        id = id + 1
                        child_attrib = child.attrib
                        child_text = child.text
                        print(child_tag + str(id)+ ": " + str(child_attrib))
                        for subchild in child:
                            subchild_tag = subchild.tag
                            if subchild_tag in xmlTag_Song_Data:
                               subchild_attrib = subchild.attrib
                               subchild_text = subchild.text
                               print(child_tag + str(id) + "_" + subchild_tag + ": " + str(subchild_attrib))
                            elif subchild_tag in xmlTag_Song_Poi:
                               i = i + 1
                               subchild_attrib = subchild.attrib
                               subchild_text = subchild.text
                               print(child_tag + str(id) + "_" + subchild_tag + str(i) + ": " + str(subchild_attrib))
                            elif subchild_tag in xmlTag_Song_Comment:
                                subchild_attrib = subchild.attrib
                                subchild_text = subchild.text
                                print(child_tag + str(id) + "_" + subchild_tag + ": " + str(subchild_text))
                            else:
                                print(f"subchild_tag < {subchild_tag} > not defined")
