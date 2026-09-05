#------------------------------------------------------------------------------------
# VirtualDJ databases
#------------------------------------------------------------------------------------
import os
import platform
from tkinter import N
import xml.etree.ElementTree as ET
from typing import Optional, Any, Union
from dataclasses import dataclass
from pathlib import Path
from enum import Enum
import sqlite3
from contextlib import closing
from datetime import datetime,timedelta

__version__ = '1.0.13'
 
#------------------------------------------------------------------------------------
def _to_float(value: Optional[str]) -> Optional[float]:
    try:
        return float(value) if value is not None else None
    except ValueError:
        return None
#------------------------------------------------------------------------------------
def _to_int(value: Optional[str]) -> Optional[int]:
    try:
        return int(value) if value is not None else None
    except ValueError:
        return None
#------------------------------------------------------------------------------------
def _to_strftime(value: Optional[str]) -> Optional[str]:
    date_value = _to_int(value)
    if date_value is None:
        return None
    try:
        date_time = datetime.fromtimestamp(date_value)
        return date_time.strftime("%Y/%m/%d %H:%M:%S%z")
    except ValueError:
        return None

#------------------------------------------------------------------------------------
def _to_bpm(value: Optional[str], digit: int = 3) -> Optional[float]:
    try:
        bpm = float(value) if value is not None else None
        if bpm is not None and bpm !=0:
            bpm = round(1 / bpm * 60, digit)
        return bpm
    except ValueError:
        return None
#------------------------------------------------------------------------------------
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
@dataclass
class VdjSongPoi:
    Name: Optional[str] = None
    Pos: Optional[float] = None
    Type: str = None
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
    FileSize: int = None
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
class VirtualDJSongsDatabase:
    XML_DATABASE_NAME = "database.xml"
    SQLITE_CACHE_DB = "cache.db"
    SQLITE_CACHE_DB_WAVEFORMS = "waveforms"
    SQLITE_EXTRA_DB = "extra.db"
    SQLITE_EXTRA_DB_LYRICS = "lyrics"
    SQLITE_EXTRA_DB_RELATED_TRACKS = "related_tracks"
    SQLITE_EXTRA_DB_TRACK_DATA = "track_data"

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
    def read_local_xml_database(self, database_path: Union[str,Path], filepath_only: bool = True) -> list[VdjSong]:
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

        VdjSong_list = [self._parse_song(song, filepath_only) for song in songs_list]

        return VdjSong_list
    #------------------------------------------------------------------------------------
    @staticmethod
    def _parse_song(song_el: ET.Element, filepath_only: bool = True) -> VdjSong:
            song_el_tag = song_el.tag
            song_el_attrib = song_el.attrib
            song_el_text = song_el.text
            song = VdjSong(
                FilePath = song_el_attrib.get("FilePath"),
                Flag = _to_int(song_el_attrib.get("Flag"))
            )
            song.FileSize = _to_int(song_el_attrib.get("FileSize"))

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
                    tags.Year = _to_int(child_attrib.get("Year"))
                    tags.Genre = child_attrib.get("Genre")
                    tags.Bpm = _to_bpm(child_attrib.get("Bpm"))
                    tags.Key = child_attrib.get("Key")
                    tags.Album = child_attrib.get("Album")
                    tags.Composer = child_attrib.get("Composer")
                    tags.Label = child_attrib.get("Label")
                    tags.TrackNumber = child_attrib.get("TrackNumber")
                    tags.Remix = child_attrib.get("Remix")
                    tags.Stars = _to_int(child_attrib.get("Stars"))
                    tags.Remixer = child_attrib.get("Remixer")
                    tags.Grouping = child_attrib.get("Grouping")
                    tags.User1 = child_attrib.get("User1")
                    tags.User2 = child_attrib.get("User2")
                    tags.Internal = child_attrib.get("Internal")
                    tags.Flag = _to_int(child_attrib.get("Flag"))
                    song.Tags = tags
                elif child_tag == "Infos":
                    infos = VdjSongInfos()
                    infos.SongLength =  _to_songlength(child_attrib.get("SongLength"))
                    infos.LastModified = _to_strftime(child_attrib.get("LastModified"))
                    infos.FirstSeen = _to_strftime(child_attrib.get("FirstSeen"))
                    infos.FirstPlay = _to_strftime(child_attrib.get("FirstPlay"))
                    infos.LastPlay = _to_strftime(child_attrib.get("LastPlay"))
                    infos.PlayCount = _to_int(child_attrib.get("PlayCount"))
                    infos.Bitrate = _to_int(child_attrib.get("Bitrate"))
                    infos.Cover = _to_int(child_attrib.get("Cover"))
                    infos.Color = _to_int(child_attrib.get("Color"))
                    infos.Corrupted = _to_int(child_attrib.get("Corrupted"))
                    infos.Gain = _to_int(child_attrib.get("Gain"))
                    infos.UserColor = child_attrib.get("UserColor")
                    song.Infos = infos
                elif child_tag == "Scan":
                    scan = VdjSongScan()
                    scan.Version = _to_int(child_attrib.get("Version"))
                    scan.Bpm = _to_bpm(child_attrib.get("Bpm"))
                    scan.Phase = _to_float(child_attrib.get("Phase"))
                    scan.AltBpm = _to_bpm(child_attrib.get("AltBpm"))
                    scan.Rigid = _to_float(child_attrib.get("Rigid"))
                    scan.Volume = _to_float(child_attrib.get("Volume"))
                    scan.Key = child_attrib.get("Key")
                    scan.AudioSig = child_attrib.get("AudioSig")
                    scan.Flag = _to_int(child_attrib.get("Flag"))
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
                    poi.Name = child_attrib.get("Name"),
                    poi.Pos = _to_float(child_attrib.get("Pos")),
                    poi.Type = child_attrib.get("Type"),
                    poi.Point = child_attrib.get("Point"),
                    poi.Num = _to_int(child_attrib.get("Num")),
                    poi.Bpm = _to_float(child_attrib.get("Bpm")),
                    poi.Phrase = _to_int(child_attrib.get("Phrase")),
                    poi.Size = _to_float(child_attrib.get("Size")),
                    poi.Slot = _to_int(child_attrib.get("Slot)"))
                    song.Poi = poi_list.append(poi)
                elif child_tag  == "Comment":
                    song.Comment = child_attrib.get("Comment")
                else:
                    print(f"child_tag < {child_tag} > not defined")
       
            return song
    #------------------------------------------------------------------------------------
    def read_local_sqlite_database(self, database_path: Union[str,Path], database_name: str, table_name: str) -> list[dict]:

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
    @staticmethod
    def _sqlite_query(database_path, sql_script) -> list[dict]:
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
            result = []

        return result