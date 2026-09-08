#------------------------------------------------------------------------------------
# VirtualDJ databases
#------------------------------------------------------------------------------------
__version__ = '1.0.19'

import xml.etree.ElementTree as ET
from typing import Optional, Union
from dataclasses import dataclass
from pathlib import Path
from enum import Enum
import sqlite3
from contextlib import closing
from datetime import datetime,timedelta

from .client_utils import VirtualDJClientUtils
from .client_config import VDJ_XML_DATABASE_NAME
from .client_config import VDJ_SQLITE_CACHE_DB, VDJ_SQLITE_CACHE_DB_WAVEFORMS, VDJ_FOLDER_CACHE
from .client_config import VDJ_SQLITE_EXTRA_DB, VDJ_SQLITE_EXTRA_DB_LYRICS, VDJ_SQLITE_EXTRA_DB_RELATED_TRACKS, VDJ_SQLITE_EXTRA_DB_TRACK_DATA

#------------------------------------------------------------------------------------
@dataclass
class VdjSongPoi:
    Name: Optional[str] = None
    Pos: Optional[float] = None
    Type: Optional[str] = None
    Point: Optional[str] = None
    Num: Optional[int] = None
    Bpm: Optional[float] = None
    Phrase: Optional[int] = None
    Size: Optional[float] = None
    Slot: Optional[int] = None
    Action: Optional[str] = None
    Color: Optional[int] = None
    #------------------------------------------------------------------------------------
    class VdjSongPoiType(str, Enum):
        AUTOMIX = "automix"
        BEATGRID = "beatgrid"
        REMIX = "remix"
        CUE = "cue"
        ACTION = "action"
        LOOP = "loop"
    #------------------------------------------------------------------------------------
    class VdjSongPoiPoint(str, Enum):
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
class VdjSongTags:
    Author: Optional[str] = None
    Title: Optional[str] = None
    Year: Optional[int] = None
    Genre: Optional[str] = None
    Bpm: Optional[float] = None
    Key: Optional[str] = None
    Album: Optional[str] = None
    Composer: Optional[str] = None
    Label: Optional[str] = None
    TrackNumber: Optional[str] = None
    Remix: Optional[str] = None
    Stars: Optional[int] = None
    Remixer: Optional[str] = None
    Grouping: Optional[str] = None
    User1: Optional[str] = None
    User2: Optional[str] = None
    Internal: Optional[str] = None
    Flag: Optional[int] = None
    #------------------------------------------------------------------------------------
    class VdjSongTagsFlag(int, Enum):
        FLAG1 = 1
#------------------------------------------------------------------------------------
@dataclass
class VdjSongInfos:
    SongLength: Optional[str] = None
    LastModified: Optional[str] = None
    FirstSeen: Optional[str] = None
    FirstPlay: Optional[str] = None
    LastPlay: Optional[str] = None
    PlayCount: Optional[int] = None
    Bitrate: Optional[int] = None
    Cover: Optional[int] = None
    Color: Optional[int] = None
    Corrupted: Optional[int] = None
    Gain: Optional[int] = None
    UserColor: Optional[str] = None
#------------------------------------------------------------------------------------
@dataclass
class VdjSongScan:
    Version: Optional[int] = None
    Bpm: Optional[float] = None
    Phase: Optional[float] = None
    AltBpm: Optional[float] = None
    Rigid: Optional[float] = None
    Volume: Optional[float] = None
    Key: Optional[str] = None
    AudioSig: Optional[str] = None
    Flag: Optional[int] = None
    BeatGrid: Optional[str] = None
    #------------------------------------------------------------------------------------
    class VdjSongScanFlag(int, Enum):
        FLAG1 = 32768 # [0x8000]
#------------------------------------------------------------------------------------
@dataclass
class VdjSongLink:
    NetSearch: Optional[str] = None
    Cover: Optional[str] = None
    clouddriveId: Optional[str] = None
#------------------------------------------------------------------------------------
@dataclass
class VdjSong:
    FilePath: Union[str,Path]
    Flag: Optional[int] = None
    FileSize: Optional[int] = None
    Tags: Optional[VdjSongTags] = None
    Infos: Optional[VdjSongInfos] = None
    Comment: Optional[str] = None
    Scan: Optional[VdjSongScan] = None
    Poi: Optional[list[VdjSongPoi]] = None
    CustomMix: Optional[str] = None
    Link: Optional[VdjSongLink] = None
    #------------------------------------------------------------------------------------
    class VdjSongFlag(int, Enum):
        HIDDEN_FROM_SEARCH = 1  # [0x01]
        FILE_NOT_FOUND = 16  # [0x10]
        KARAOKE_FILE = 32  # [0x20]
        VIDEO_FILE = 64  # [0x40]
        NETSEARCH_FILE = 256 # [0x100]
#------------------------------------------------------------------------------------ 
class VirtualDJSongsDatabase():
    def __init__(self):
        self.vdj_utils = VirtualDJClientUtils()
        self.XML_DATABASE_NAME = VDJ_XML_DATABASE_NAME
        self.SQLITE_CACHE_DB = VDJ_SQLITE_CACHE_DB
        self.SQLITE_CACHE_DB_WAVEFORMS = VDJ_SQLITE_CACHE_DB_WAVEFORMS
        self.FOLDER_CACHE = VDJ_FOLDER_CACHE
        self.SQLITE_EXTRA_DB = VDJ_SQLITE_EXTRA_DB
        self.SQLITE_EXTRA_DB_LYRICS = VDJ_SQLITE_EXTRA_DB_LYRICS
        self.SQLITE_EXTRA_DB_RELATED_TRACKS = VDJ_SQLITE_EXTRA_DB_RELATED_TRACKS
        self.SQLITE_EXTRA_DB_TRACK_DATA = VDJ_SQLITE_EXTRA_DB_TRACK_DATA
    #------------------------------------------------------------------------------------
    def get_local_database_list(self) -> list[Path]:
        database_list : list[Path]= []

        vdj_home_list = self.vdj_utils.get_virtualdj_home_list()
        for vdj_home in vdj_home_list:
            main_XMLdatabase_path = vdj_home / self.XML_DATABASE_NAME
            if main_XMLdatabase_path.exists():
                database_list.append(main_XMLdatabase_path)
            main_SQLite1database_path = vdj_home / self.SQLITE_EXTRA_DB
            if main_SQLite1database_path.exists():
                database_list.append(main_SQLite1database_path)
            main_SQLite2database_path = vdj_home / self.FOLDER_CACHE / self.SQLITE_CACHE_DB
            if main_SQLite2database_path.exists():
                database_list.append(main_SQLite2database_path)


        vdj_home_ext_list = self.vdj_utils.get_virtualdj_home_ext_list()
        for vdj_home_ext in vdj_home_ext_list:
            external_XMLdatabase_path = vdj_home_ext / self.XML_DATABASE_NAME
            if external_XMLdatabase_path.exists():
                database_list.append(external_XMLdatabase_path)
            external_SQLite1database_path = vdj_home_ext / self.SQLITE_EXTRA_DB
            if external_SQLite1database_path.exists():
                database_list.append(external_SQLite1database_path)
            external_SQLite2database_path = vdj_home_ext / self.FOLDER_CACHE/ self.SQLITE_CACHE_DB
            if external_SQLite2database_path.exists():
                database_list.append(external_SQLite2database_path)

        database_list_noduplicates = list(dict.fromkeys(database_list))

        return database_list_noduplicates
    #------------------------------------------------------------------------------------
    def read_local_xml_database(self, database_path: Path, filepath_only: bool = True) -> list[VdjSong]:
        try:
            tree = ET.parse(database_path)
        except ET.ParseError as exc:
            print(f"VirtualDJ database reading {database_path} => Invalid XML file")
            self.vdj_utils.SaveClientLog(f"VirtualDJ database reading {database_path} => Invalid XML file")
            return []
        except OSError as exc:
            print(f"VirtualDJ database reading {database_path} => Cannot read database")
            self.vdj_utils.SaveClientLog(f"VirtualDJ database reading {database_path} => Cannot read database")
            return []

        root = tree.getroot()
        root_tag = root.tag
        root_attrib = root.attrib
        if root_tag != "VirtualDJ_Database":
            print(f"VirtualDJ database reading {database_path} => Not a VirtualDJ database")
            self.vdj_utils.SaveClientLog(f"VirtualDJ database reading {database_path} => Not a VirtualDJ database")
            return []

        songs_list = root.findall(".//Song")        
        songs_list_count = len(songs_list)

        print(f"VirtualDJ database reading => {root_attrib}")
        self.vdj_utils.SaveClientLog(f"VirtualDJ database reading {database_path} => {root_attrib}")

        print(f"VirtualDJ database reading => Number of songs found = {songs_list_count}")
        self.vdj_utils.SaveClientLog(f"VirtualDJ database reading {database_path} => Number of songs found = {songs_list_count}")


        VdjSong_list = [self._parse_song(song, filepath_only) for song in songs_list]

        return VdjSong_list
    #------------------------------------------------------------------------------------
    @staticmethod
    def _to_float(value: Optional[str]) -> Optional[float]:
        try:
            return float(value) if value is not None else None
        except ValueError:
            return None
    #------------------------------------------------------------------------------------
    @staticmethod
    def _to_int(value: Optional[str]) -> Optional[int]:
        try:
            return int(value) if value is not None else None
        except ValueError:
            return None
    #------------------------------------------------------------------------------------
    @staticmethod
    def _to_strftime(value: Optional[str]) -> Optional[str]:
        try:
            date_value = int(value) if value is not None else None
            if date_value is None:
                return None
            date_time = datetime.fromtimestamp(date_value)
            return date_time.strftime("%Y/%m/%d %H:%M:%S%z")
        except ValueError:
            return None

    #------------------------------------------------------------------------------------
    @staticmethod
    def _to_bpm(value: Optional[str], digit: int = 3) -> Optional[float]:
        """ Conversion of the Bpm from the VirtualDJ format """
        try:
            bpm = float(value) if value is not None else None
            if bpm is not None and bpm !=0:
                bpm = round(1 / bpm * 60, digit)
            return bpm
        except ValueError:
            return None
    #------------------------------------------------------------------------------------
    @staticmethod
    def _to_songlength(value: Optional[str]) -> Optional[str]:
        try:
            seconds = float(value) if value is not None else None
            if seconds is None:
                return None
            songlength = str(timedelta(seconds=seconds))
            return songlength
        except ValueError:
            return None
    #------------------------------------------------------------------------------------
    def _parse_song(self, song_el: ET.Element, filepath_only: bool = True) -> VdjSong:
            song_el_tag = song_el.tag
            song_el_attrib = song_el.attrib
            song_el_text = song_el.text
            song = VdjSong(
                FilePath = song_el_attrib.get("FilePath"),
                Flag = self._to_int(song_el_attrib.get("Flag"))
            )
            song.FileSize = self._to_int(song_el_attrib.get("FileSize"))

            if filepath_only:
                return song

            poi_list = []

            for child in song_el:
                child_tag = child.tag
                child_attrib = child.attrib
                child_text = child.text
                if child_tag == "Tags":
                    tags = VdjSongTags()
                    tags.Author = child_attrib.get("Author")
                    tags.Title = child_attrib.get("Title")
                    tags.Year = self._to_int(child_attrib.get("Year"))
                    tags.Genre = child_attrib.get("Genre")
                    tags.Bpm = self._to_bpm(child_attrib.get("Bpm"))
                    tags.Key = child_attrib.get("Key")
                    tags.Album = child_attrib.get("Album")
                    tags.Composer = child_attrib.get("Composer")
                    tags.Label = child_attrib.get("Label")
                    tags.TrackNumber = child_attrib.get("TrackNumber")
                    tags.Remix = child_attrib.get("Remix")
                    tags.Stars = self._to_int(child_attrib.get("Stars"))
                    tags.Remixer = child_attrib.get("Remixer")
                    tags.Grouping = child_attrib.get("Grouping")
                    tags.User1 = child_attrib.get("User1")
                    tags.User2 = child_attrib.get("User2")
                    tags.Internal = child_attrib.get("Internal")
                    tags.Flag = self._to_int(child_attrib.get("Flag"))
                    song.Tags = tags
                elif child_tag == "Infos":
                    infos = VdjSongInfos()
                    infos.SongLength =  self._to_songlength(child_attrib.get("SongLength"))
                    infos.LastModified = self._to_strftime(child_attrib.get("LastModified"))
                    infos.FirstSeen = self._to_strftime(child_attrib.get("FirstSeen"))
                    infos.FirstPlay = self._to_strftime(child_attrib.get("FirstPlay"))
                    infos.LastPlay = self._to_strftime(child_attrib.get("LastPlay"))
                    infos.PlayCount = self._to_int(child_attrib.get("PlayCount"))
                    infos.Bitrate = self._to_int(child_attrib.get("Bitrate"))
                    infos.Cover = self._to_int(child_attrib.get("Cover"))
                    infos.Color = self._to_int(child_attrib.get("Color"))
                    infos.Corrupted = self._to_int(child_attrib.get("Corrupted"))
                    infos.Gain = self._to_int(child_attrib.get("Gain"))
                    infos.UserColor = child_attrib.get("UserColor")
                    song.Infos = infos
                elif child_tag == "Scan":
                    scan = VdjSongScan()
                    scan.Version = self._to_int(child_attrib.get("Version"))
                    scan.Bpm = self._to_bpm(child_attrib.get("Bpm"))
                    scan.Phase = self._to_float(child_attrib.get("Phase"))
                    scan.AltBpm = self._to_bpm(child_attrib.get("AltBpm"))
                    scan.Rigid = self._to_float(child_attrib.get("Rigid"))
                    scan.Volume = self._to_float(child_attrib.get("Volume"))
                    scan.Key = child_attrib.get("Key")
                    scan.AudioSig = child_attrib.get("AudioSig")
                    scan.Flag = self._to_int(child_attrib.get("Flag"))
                    scan.BeatGrid = child_attrib.get("BeatGrid")
                    song.Scan = scan
                elif child_tag == "CustomMix":
                    song.CustomMix = child_attrib.get("CustomMix")
                elif child_tag == "Link":
                    link = VdjSongLink()
                    link.NetSearch = child_attrib.get("NetSearch")
                    link.Cover = child_attrib.get("Cover")
                    link.clouddriveId = child_attrib.get("clouddriveId")
                    song.Link = link
                elif child_tag == "Poi":
                    poi = VdjSongPoi()
                    poi.Name = child_attrib.get("Name")
                    poi.Pos = self._to_float(child_attrib.get("Pos"))
                    poi.Type = child_attrib.get("Type")
                    poi.Point = child_attrib.get("Point")
                    poi.Num = self._to_int(child_attrib.get("Num"))
                    poi.Bpm = self._to_float(child_attrib.get("Bpm"))
                    poi.Phrase = self._to_int(child_attrib.get("Phrase"))
                    poi.Size = self._to_float(child_attrib.get("Size"))
                    poi.Slot = self._to_int(child_attrib.get("Slot"))
                    poi.Action = child_attrib.get("Action")
                    poi.Color = self._to_int(child_attrib.get("Color"))
                    poi_list.append(poi)
                elif child_tag  == "Comment":
                    song.Comment = child_attrib.get("Comment")
                else:
                    print(f"child_tag < {child_tag} > not defined")
                    self.vdj_utils.SaveClientLog(f"child_tag < {child_tag} > not defined")
            
            # We add Poi list outside of the loop
            song.Poi = poi_list or None
       
            return song
    #------------------------------------------------------------------------------------
    def read_local_sqlite_database(self, database_path: Path, database_name: str, table_name: str) -> list[dict]:

        if database_name == self.SQLITE_CACHE_DB:
            if table_name == self.SQLITE_CACHE_DB_WAVEFORMS:
                # waveforms: id[INTEGER, PRIMARY_KEY], filepath[TEXT], filename[TEXT], filesize[INTEGER], type[INTEGER], version[INTEGER], valuesPerSecond[REAL], waveform[BLOB]
                sql_script = f"SELECT * FROM {table_name}"
            else:
                sql_script = ""
        elif database_name == self.SQLITE_EXTRA_DB:
            if table_name == self.SQLITE_EXTRA_DB_LYRICS:
                # lyrics : lid[BLOB,PRIMARY_KEY], xml[TEXT]
                sql_script = f"SELECT * FROM {table_name}"
            elif table_name == self.SQLITE_EXTRA_DB_RELATED_TRACKS:
                # related_tracks: id[INTEGER,PRIMARY_KEY], sid1[INTEGER], sid2[INTEGER]
                sql_script = f"SELECT * FROM {table_name}"
            elif table_name == self.SQLITE_EXTRA_DB_TRACK_DATA:
                # track_data: id[INTEGER,PRIMARY_KEY], sid[INTEGER], file[TEXT], filesize[INTEGER], artist[TEXT], title[TEXT], remix[TEXT]
                sql_script = f"SELECT * FROM {table_name}"
            else:
                sql_script = ""
        else:
            sql_script = ""


        if sql_script == "":
            return []

        result_list = []
        print(sql_script)
        result_list = self._sqlite_query(database_path, sql_script)

        return result_list
    #------------------------------------------------------------------------------------
    def _sqlite_query(self, database_path: Path, sql_script) -> list[dict]:
        result = []
        try:
           with sqlite3.connect(database_path) as connection:
               connection.row_factory = sqlite3.Row
               with closing(connection.cursor()) as cursor:
                    rows = cursor.execute(sql_script).fetchall()
                    for row in rows:
                        value = dict(row)
                        result.append(value)
        except Exception as e:
            print(f"Failed to query the sqlite database: ", str(e))
            self.vdj_utils.SaveClientLog(f"Failed to query the sqlite database: ", str(e))
            result = []

        return result