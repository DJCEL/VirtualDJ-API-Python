#------------------------------------------------------------------------------------
# VirtualDJ databases
#------------------------------------------------------------------------------------
import os
import platform
import xml.etree.ElementTree as ET
from typing import Optional, Any, Union
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum

__version__ = '1.0.6'
 
#------------------------------------------------------------------------------------
def _to_float(value: Optional[str]) -> Optional[float]:
    try:
        return float(value) if value  is not None else None
    except ValueError:
        return None
#------------------------------------------------------------------------------------
def _to_int(value: Optional[str]) -> Optional[int]:
    try:
        return int(value) if value  is not None else None
    except ValueError:
        return None
#------------------------------------------------------------------------------------
@dataclass
class VdjPoi:
        name: Optional[str] = None
        pos: Optional[float] = None
        type: Optional[str] = None
        point: Optional[str] = None
        num: Optional[int] = None
        bpm: Optional[float] = None
        phrase: Optional[int] = None
        size: Optional[float] = None
        slot: Optional[int] = None
        #------------------------------------------------------------------------------------
        class VdjPoiType(str, Enum):
            AUTOMIX = "automix"
            BEATGRID = "beatgrid"
            REMIX = "remix"
        #------------------------------------------------------------------------------------
        class VdjPoiPoint(str, Enum):
            REAL_START = "realStart"
            REAL_END = "realEnd"
            FADE_START = "fadeStart"
            FADE_END = "fadeEnd"
            CUT_START = "cutStart"
            CUT_END = "cutEnd"
            TEMPO_START = "tempoStart"
            TEMPO_END = "tempoEnd"
#------------------------------------------------------------------------------------
@dataclass
class VdjSong:
       FilePath: Union[str,Path]
       Flag: int
       FileSize: Optional[int] = None
       Tags_Author: Optional[str] = None
       Tags_Title: Optional[str] = None
       Tags_Year: Optional[int] = None
       Tags_Genre: Optional[str] = None
       Tags_Bpm: Optional[float] = None
       Tags_Key: Optional[str] = None
       Tags_Album: Optional[str] = None
       Tags_Composer: Optional[str] = None
       Tags_Label: Optional[str] = None
       Tags_TrackNumber: Optional[str] = None
       Tags_Remix: Optional[str] = None
       Tags_Stars: Optional[int] = None
       Tags_Remixer: Optional[str] = None
       Tags_Grouping: Optional[str] = None
       Tags_User1: Optional[str] = None
       Tags_User2: Optional[str] = None
       Tags_Internal: Optional[str] = None
       Tags_Flag: Optional[int] = None
       Infos_SongLength: Optional[float] = None
       Infos_LastModified: Optional[int] = None
       Infos_FirstSeen: Optional[int] = None
       Infos_FirstPlay: Optional[int] = None
       Infos_LastPlay: Optional[int] = None
       Infos_PlayCount: Optional[int] = None
       Infos_Bitrate: Optional[int] = None
       Infos_Cover: Optional[int] = None
       Infos_Color: Optional[int] = None
       Infos_Corrupted: Optional[int] = None
       Infos_Gain: Optional[int] = None
       Infos_UserColor: Optional[str] = None
       Comment: Optional[str] = None
       Scan_Version: Optional[int] = None
       Scan_Bpm: Optional[float] = None
       Scan_Phase: Optional[float] = None
       Scan_AltBpm: Optional[float] = None
       Scan_Rigid: Optional[float] = None
       Scan_Volume: Optional[float] = None
       Scan_Key: Optional[str] = None
       Scan_AudioSig: Optional[str] = None
       Scan_Flag: Optional[int] = None
       Scan_Beatgrid: Optional[list[str]] = None
       Poi: Optional[list[VdjPoi]] = None
       CustomMix: Optional[str] = None
       Link_NetSearch: Optional[str] = None
       Link_Cover: Optional[str] = None
       Link_clouddriveId: Optional[str] = None
#------------------------------------------------------------------------------------ 
class VirtualDJSongsDatabase:
    XML_DATABASE_NAME = "database.xml"
    SQLITE_EXTRA_DB = "extra.db"
    SQLITE_CACHE_DB = "cache.db"
    SQLITE_EXTRA_DB_TABLES = ["lyrics","related_tracks","track_data"]
    SQLITE_CACHE_DB_TABLES = ["waveforms"]
    #------------------------------------------------------------------------------------
    def get_local_database_list(self) -> list[Path]:
        system = platform.system()
        database_list : list[Path]= []

        if system == "Windows":
            local_appdata = os.getenv('LOCALAPPDATA')
            if local_appdata:
                main_XMLdatabase_path = os.path.join(local_appdata, 'VirtualDJ', self.XML_DATABASE_NAME)
                if os.path.exists(main_XMLdatabase_path):
                    database_list.append(main_XMLdatabase_path)
                main_SQLite1database_path = os.path.join(local_appdata,'VirtualDJ', self.SQLITE_EXTRA_DB)
                if os.path.exists(main_SQLite1database_path):
                    database_list.append(main_SQLite1database_path)
                main_SQLite2database_path = os.path.join(local_appdata,'VirtualDJ', 'Cache', self.SQLITE_CACHE_DB)
                if os.path.exists(main_SQLite2database_path):
                    database_list.append(main_SQLite2database_path)

            drives_Windows = self._windows_drive_roots()
            for drive in drives_Windows:
                drive_full = drive + "\\"
                external_XMLdatabase_path = os.path.join(drive_full,'VirtualDJ', self.XML_DATABASE_NAME)
                if os.path.exists(external_XMLdatabase_path):
                    database_list.append(external_XMLdatabase_path)
                external_SQLite1database_path = os.path.join(drive_full,'VirtualDJ', self.SQLITE_EXTRA_DB)
                if os.path.exists(external_SQLite1database_path):
                    database_list.append(external_SQLite1database_path)
                external_SQLite2database_path = os.path.join(drive_full,'VirtualDJ', 'Cache', self.SQLITE_CACHE_DB)
                if os.path.exists(external_SQLite2database_path):
                    database_list.append(external_SQLite2database_path)

            database_list_noduplicates = list(dict.fromkeys(database_list))

            return database_list_noduplicates

        elif system == "Darwin":
            # Path.home() / "Library" / 
            return database_list

        return database_list
    #------------------------------------------------------------------------------------
    @staticmethod
    def _windows_drive_roots() -> list[Path]:
        drives_Windows = [ chr(x) + ":" for x in range(65,91) if os.path.exists(chr(x) + ":") ]
        return drives_Windows
    #------------------------------------------------------------------------------------
    def read_local_xml_database(self, database_path: Union[str,Path], read_all_songs: bool = False) -> list[VdjSong]:
        try:
            tree = ET.parse(database_path)
        except ET.ParseError as exc:
            print(f"Invalid VirtualDJ XML database: {database_path}")
            return []
        except OSError as exc:
            print(f"Cannot read database: {database_path}")
            return []

        root = tree.getroot()
        root_tag = root.tag
        root_attrib = root.attrib
        if root_tag != "VirtualDJ_Database":
            print(f"Not a VirtualDJ database file: {database_path}")
            return []


        
        songs_list = root.findall(".//Song")        
        songs_list_count = len(songs_list)

        print(f"VirtualDJ database reading => {root_attrib}")
        print(f"VirtualDJ database reading => Number of songs found = {songs_list_count}")

        if not read_all_songs:
            return []

        id = 0
    
        return [self._parse_song(id, song) for song in songs_list]
    #------------------------------------------------------------------------------------
    @staticmethod
    def _parse_song(id:int, song_el: ET.Element) -> VdjSong:
            song_el_tag = song_el.tag
            song_el_attrib = song_el.attrib
            song_el_text = song_el.text
            id = id + 1
            #print(song_el_tag + str(id)+ ": " + str(song_el_attrib))
            song = VdjSong(
                FilePath = song_el_attrib.get("FilePath"),
                Flag = _to_int(song_el_attrib.get("Flag"))
            )

            song.FileSize = _to_int(song_el_attrib.get("FileSize"))

            poi_list = []

            i = 0
            for subchild in song_el:
                subchild_tag = subchild.tag
                subchild_attrib = subchild.attrib
                subchild_text = subchild.text
                if subchild_tag == "Tags":
                    #print(song_el_tag + str(id) + "_" + subchild_tag + ": " + str(subchild_attrib))
                    song.Tags_Author = subchild_attrib.get("Author")
                    song.Tags_Title = subchild_attrib.get("Title")
                    song.Tags_Remix = subchild_attrib.get("Remix")
                elif subchild_tag == "Infos":
                    #print(song_el_tag + str(id) + "_" + subchild_tag + ": " + str(subchild_attrib))
                    song.Infos_SongLength =  _to_float(subchild_attrib.get("SongLength"))
                elif subchild_tag == "Scan":
                    #print(song_el_tag + str(id) + "_" + subchild_tag + ": " + str(subchild_attrib))
                    song.Scan_Version =  _to_int(subchild_attrib.get("Version"))
                    song.Scan_Flag =  _to_int(subchild_attrib.get("Flag"))
                    song.Scan_Bpm =  _to_float(subchild_attrib.get("Bpm"))
                    song.Scan_Key =  subchild_attrib.get("Key")
                    song.Scan_Phase =  subchild_attrib.get("Phase")
                elif subchild_tag == "CustomMix":
                    #print(song_el_tag + str(id) + "_" + subchild_tag + ": " + str(subchild_attrib))
                elif subchild_tag == "Link":
                    #print(song_el_tag + str(id) + "_" + subchild_tag + ": " + str(subchild_attrib))
                elif subchild_tag == "Poi":
                    i = i + 1
                    #print(song_el_tag + str(id) + "_" + subchild_tag + str(i) + ": " + str(subchild_attrib))
                    poi = VdjPoi(
                        name = subchild_attrib.get("Name"),
                        pos = _to_float(attrib.get("Pos")),
                        type = subchild_attrib.get("Type"),
                        point = subchild_attrib.get("Point"),
                        num = _to_int(subchild_attrib.get("Num")),
                        bpm = _to_float(subchild_attrib.get("Bpm")),
                        phrase = _to_int(subchild_attrib.get("Phrase")),
                        size = _to_float(subchild_attrib.get("Size")),
                        slot = _to_int(subchild_attrib.get("Slot)"))
                    )
                    song.Poi = poi_list.append(poi)
                elif subchild_tag  == "Comment":
                    #print(song_el_tag + str(id) + "_" + subchild_tag + ": " + str(subchild_text))
                    song.Comment = subchild_attrib.get("Comment")
                else:
                    print(f"subchild_tag < {subchild_tag} > not defined")
       
            return song