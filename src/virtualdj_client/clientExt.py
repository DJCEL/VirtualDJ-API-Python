#------------------------------------------------------------------------------------
# VirtualDJ ClientExt
#------------------------------------------------------------------------------------
__version__ = "1.0.0"

import asyncio
from typing import Optional, Literal
from dataclasses import dataclass

from .client import VirtualDJClient

#------------------------------------------------------------------------------------------------------------------------------------
@dataclass
class VDJDeck:
    name: Literal['left', 'right', 'leftvideo', 'rightvideo', 'all', 'default', 'active', 'master'] = None
    id: int = None
#------------------------------------------------------------------------------------------------------------------------------------
@dataclass
class VdjDeckData:
    Filepath: Optional[str] = None
    Filesize: Optional[int] = None
    Artist: Optional[str] = None
    Title: Optional[str] = None
    Remix: Optional[str] = None
    Genre: Optional[str] = None
    Album: Optional[str] = None
    Year: Optional[str] = None
    Comment: Optional[str] = None
    Bpm: Optional[float] = None
    BpmCurrent: Optional[float] = None
    Key: Optional[str] = None
    KeyHarmonic: Optional[str] = None
    KeyCurrent: Optional[str] = None
    KeyCurrentHarmonic: Optional[str] = None
    Duration: Optional[float] = None
    Position: Optional[float] = None
    Time: Optional[float] = None
    Beat: Optional[float] = None 
    Volume: Optional[float] = None
    Level: Optional[float] = None
    LoopSize: Optional[int] = None
    Pitch: Optional[float] = None 

#------------------------------------------------------------------------------------------------------------------------------------
class VirtualDJClientExt():
    def __init__(self):
        self.client = VirtualDJClient()
    #------------------------------------------------------------------------------------
    def is_app_running(self) -> bool:
        return self.client.is_app_running()
    #------------------------------------------------------------------------------------
    def open_app(self) -> bool:
        return self.client.open_app()
    #------------------------------------------------------------------------------------
    def close_app(self) -> bool:
        return self.client.close_app()
    #------------------------------------------------------------------------------------
    def is_connected(self) -> bool:
        return self.client.is_connected()
    #------------------------------------------------------------------------------------
    @staticmethod
    def vdjscript_and(vdj_script1:str, vdj_script2:str) -> str:
        vdj_script_full = vdj_script1 + ' & ' + vdj_script2
        return vdj_script_full
    #------------------------------------------------------------------------------------
    @staticmethod
    def vdjscript_if_then_else(vdj_script_condition:str, vdj_script_if_true:str, vdj_script_if_false:str) -> str:
        vdj_script_full = vdj_script_condition + ' ? ' + vdj_script_if_true + " : " + vdj_script_if_false
        return vdj_script_full
    #------------------------------------------------------------------------------------
    async def _get_result(self, deck: str, verb: str) -> str:
        vdj_script = f"deck {deck} {verb}"
        result = await self.client.get_async(vdj_script)
        result_check = result[0:15]
        if result_check == 'Failed to query':
            return None
        return result
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
    #------------------------------------------------------------------------------------------------------------------------------------
    async def get_DeckData_async(self, deck: str) -> VdjDeckData:
        deckdata = VdjDeckData()
        deckdata.Filepath = await self._get_result(deck, "get_filepath")
        deckdata.Filesize = self._to_int(await self._get_result(deck, "get_filesize"))
        deckdata.Artist = await self._get_result(deck, "get_artist")
        deckdata.Title = await self._get_result(deck, "get_title")
        deckdata.Remix = await self._get_result(deck, "get_remix")
        deckdata.Genre = await self._get_result(deck, "get_genre")
        deckdata.Album = await self._get_result(deck, "get_album")
        deckdata.Year = await self._get_result(deck, "get_year")
        deckdata.Comment = await self._get_result(deck, "get_comment")
        deckdata.Bpm = self._to_float(await self._get_result(deck, "get_bpm absolute"))
        deckdata.BpmCurrent = self._to_float(await self._get_result(deck, "get_bpm"))
        deckdata.KeyCurrent = await self._get_result(deck, "get_key 'musical'")
        deckdata.KeyCurrentHarmonic = await self._get_result(deck, "get_harmonic")
        deckdata.Duration = self._to_float(await self._get_result(deck, "get_songlength"))
        deckdata.Position = self._to_float(await self._get_result(deck, "get_position"))
        deckdata.Time = self._to_float(await self._get_result(deck, "get_time"))
        deckdata.Beat = self._to_float(await self._get_result(deck, "get_beat"))
        deckdata.Volume = self._to_float(await self._get_result(deck, "get_volume"))
        deckdata.Level = self._to_float(await self._get_result(deck, "get_level"))
        deckdata.LoopSize = self._to_int(await self._get_result(deck, "get_loop"))
        deckdata.Pitch = self._to_int(await self._get_result(deck, "get_pitch"))
        return deckdata
    #------------------------------------------------------------------------------------------------------------------------------------
    def get_DeckData(self, deck: str) -> VdjDeckData:
        return asyncio.run(self.get_DeckData_async(deck))


