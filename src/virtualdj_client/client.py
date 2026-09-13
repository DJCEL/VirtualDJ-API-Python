#------------------------------------------------------------------------------------
# VirtualDJ Client
#------------------------------------------------------------------------------------
__version__ = "1.0.23"

import asyncio
from typing import Optional, Literal
from dataclasses import dataclass

from .client_http import VirtualDJClientHttp, VdjResponse
from .client_utils import VirtualDJUtils

#------------------------------------------------------------------------------------------------------------------------------------
@dataclass
class VdjDeck:
    name: Literal['left', 'right', 'leftvideo', 'rightvideo', 'all', 'default', 'active', 'master'] | None = None
    id: int | None = None
#------------------------------------------------------------------------------------------------------------------------------------
@dataclass
class VdjDeckData:
    Filepath: Optional[str] = None
    Filesize: Optional[int] = None
    Artist: Optional[str] = None
    Title: Optional[str] = None
    Remix: Optional[str] = None
    Album: Optional[str] = None
    Genre: Optional[str] = None
    Year: Optional[int] = None
    Rating: Optional[int] = None
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
    Beatgrid: Optional[float] = None 
    Beatpos: Optional[float] = None
    Firstbeat: Optional[float] = None
    Volume: Optional[float] = None
    Level: Optional[float] = None
    LoopSize: Optional[int] = None
    Pitch: Optional[float] = None
    IsPlaying: Optional[bool] = None
    IsLooping: Optional[bool] = None
    IsReverse: Optional[bool] = None
    IsSync: Optional[bool] = None
    IsBeatlock: Optional[bool] = None
    IsMasterTempo: Optional[bool] = None
    IsKeylock: Optional[bool] = None
    HasStems: Optional[bool] = None
    HasLyrics: Optional[bool] = None
    HasError: Optional[str] = None
    IsVideo: Optional[bool] = None
    IsPfl: Optional[bool] = None
    HasLinkedTracks: Optional[bool] = None
#------------------------------------------------------------------------------------------------------------------------------------
class VirtualDJClient():
    def __init__(self):
        self.vdj_client = VirtualDJClientHttp()
        self.vdj_utils = VirtualDJUtils()
    #------------------------------------------------------------------------------------
    #  Check if VirtualDJ is connected
    #------------------------------------------------------------------------------------
    async def is_connected_async(self) -> bool:
        """ Check if Network Control Plugin is responding """
        vdj_response = await self.vdj_client.query("get_version")
        status = vdj_response.status
        status_code = vdj_response.status_code
        result = vdj_response.result

            self.vdj_utils.save_client_log(f"HTTP {status_code}:{status} / {result}")
        if status == "ok":
           return True
        else:
            return False
 #------------------------------------------------------------------------------------
    #  Launch / Quit VirtualDJ
    #------------------------------------------------------------------------------------
    def is_app_running(self) -> bool:
        """ Check if VirtualDJ software is running """
        return self.vdj_utils.is_virtualdj_running()
    #------------------------------------------------------------------------------------
    def open_app(self) -> bool:
        """ Open VirtuaDJ if not open """
        is_vdj_running = self.is_app_running()
        if is_vdj_running == True:
            return True

        # TODO: check if updates are activated in VirtualDJ via settings.xml

        bRes = self.vdj_utils.launch_virtualdj_software()
        return bRes 
    #------------------------------------------------------------------------------------
    async def get_loadSecurity_async(self) -> bool:
        vdjscript = 'setting "loadSecurity"'
        result = await self.get_async(vdjscript)
        if result in ['on','silent']:
           print("VirtualDJ => loadSecurity option is activated")
           self.vdj_utils.save_client_log("VirtualDJ => loadSecurity option is activated")
           return True
        else:
           print("VirtualDJ => loadSecurity option is disable")
           self.vdj_utils.save_client_log("VirtualDJ => loadSecurity option is disable")
           return False    
    #------------------------------------------------------------------------------------
    async def disable_loadSecurity_async(self):
        vdjscript = 'setting "loadSecurity" off'
        result = await self.send_async(vdjscript)
        if result == True:
            print("VirtualDJ => loadSecurity option is now disable")
            self.vdj_utils.save_client_log("VirtualDJ => loadSecurity option is now disable")
    #------------------------------------------------------------------------------------
    async def close_app_async(self, force_close: bool = False) -> bool:
        """ Close VirtuaDJ """
        is_vdj_running = self.is_app_running()
        if is_vdj_running == False:
            return True

        is_vdj_connected = await self.is_connected_async()
        if is_vdj_connected == True:
            is_vdj_security = await self.get_loadSecurity_async()
            if is_vdj_security and force_close:
                await self.disable_loadSecurity_async()

            # Close VirtualDJ
            result = await self.send_async("close")
            if result == True:
                return True

        # TODO: Force kill app if (force_close == True)
        return False
    #------------------------------------------------------------------------------------
    #  VirtualDJ Get/Send
    #------------------------------------------------------------------------------------
    async def get_async(self, vdjscript: str) -> str:
        """ Query VirtualDJ with a vdjscript """
        vdj_response = await self.vdj_client.query(vdjscript)
        status = vdj_response.status
        status_code = vdj_response.status_code
        result = vdj_response.result
        if status == "ok": 
            return result
        else:
            self.vdj_utils.save_client_log(f"HTTP error {status_code}: {result}")
            return result           
    #------------------------------------------------------------------------------------
    async def send_async(self, vdjscript: str) -> bool:
        """ Execute a vdjscript and return status """
        vdj_response = await self.vdj_client.execute(vdjscript)
        status = vdj_response.status
        status_code = vdj_response.status_code
        result = vdj_response.result
        if status == "ok":
            bRes = (result.lower() == "true")
            return bRes
        else:
            self.vdj_utils.save_client_log(f"HTTP error {status_code}: {result}")
            return False
    #------------------------------------------------------------------------------------
    #  Vdjscript Helper
    #------------------------------------------------------------------------------------
    @staticmethod
    def vdjscript_and(vdjscript1:str, vdjscript2:str) -> str:
        vdjscript_full = vdjscript1 + ' & ' + vdjscript2
        return vdjscript_full
    #------------------------------------------------------------------------------------
    @staticmethod
    def vdjscript_if_then_else(vdjscript_condition:str, vdjscript_if_true:str, vdjscript_if_false:str) -> str:
        vdjscript_full = vdjscript_condition + ' ? ' + vdjscript_if_true + " : " + vdjscript_if_false
        return vdjscript_full
    #------------------------------------------------------------------------------------
    #  Format conversion
    #------------------------------------------------------------------------------------
    @staticmethod
    def to_str(value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        elif value == '':
            return None
        else:
            return value
    #------------------------------------------------------------------------------------
    @staticmethod
    def to_float(value: Optional[str]) -> Optional[float]:
        if value is None:
            return None
        try:
            return float(value)
        except ValueError:
            return None
    #------------------------------------------------------------------------------------
    @staticmethod
    def to_int(value: Optional[str]) -> Optional[int]:
        if value is None:
            return None
        try:
            return int(value)
        except ValueError:
            return None
    #------------------------------------------------------------------------------------
    @staticmethod
    def to_bool(value: Optional[str]) -> Optional[bool]:
        if value is None:
            return None
        try:
            return value.lower() in ('yes','true','on','1')
        except ValueError:
            return None
    #------------------------------------------------------------------------------------
    #  get_DeckData()
    #------------------------------------------------------------------------------------  
    async def _get_result(self, deck: str, verb: str) -> str:
        vdjscript = f"deck {deck} {verb}"
        result = await self.get_async(vdjscript)
        result_check = result[0:5]
        if result_check == 'error':
            return None
        return result
    #------------------------------------------------------------------------------------
    async def get_DeckData_async(self, deck: str) -> VdjDeckData:
        deckdata = VdjDeckData()
        deckdata.Filepath = self.to_str(await self._get_result(deck, "get_filepath"))
        deckdata.Filesize = self.to_int(await self._get_result(deck, "get_filesize"))
        deckdata.Artist = self.to_str(await self._get_result(deck, "get_artist"))
        deckdata.Title = self.to_str(await self._get_result(deck, "get_title"))
        deckdata.Remix = self.to_str(await self._get_result(deck, "get_remix"))
        deckdata.Genre = self.to_str(await self._get_result(deck, "get_genre"))
        deckdata.Album = self.to_str(await self._get_result(deck, "get_album"))
        year_tmp = self.to_int(await self._get_result(deck, "get_year"))
        deckdata.Year = None if year_tmp == 0 else year_tmp
        deckdata.Rating = self.to_int(await self._get_result(deck, "rating"))
        deckdata.Comment = self.to_str(await self._get_result(deck, "get_comment"))
        deckdata.Bpm = self.to_float(await self._get_result(deck, "get_bpm absolute"))
        deckdata.BpmCurrent = self.to_float(await self._get_result(deck, "get_bpm"))
        deckdata.KeyCurrent = self.to_str(await self._get_result(deck, "get_key 'musical'"))
        deckdata.KeyCurrentHarmonic = self.to_str(await self._get_result(deck, "get_harmonic"))
        deckdata.Duration = self.to_float(await self._get_result(deck, "get_songlength"))
        deckdata.Position = self.to_float(await self._get_result(deck, "get_position"))
        deckdata.Time = self.to_float(await self._get_result(deck, "get_time"))
        deckdata.Beat = self.to_float(await self._get_result(deck, "get_beat"))
        deckdata.Beatgrid = self.to_float(await self._get_result(deck, "get_beatgrid"))
        deckdata.Beatpos = self.to_float(await self._get_result(deck, "get_beatpos"))
        deckdata.Firstbeat = self.to_float(await self._get_result(deck, "get_firstbeat"))
        deckdata.Volume = self.to_float(await self._get_result(deck, "get_volume"))
        deckdata.Level = self.to_float(await self._get_result(deck, "get_level"))
        deckdata.LoopSize = self.to_int(await self._get_result(deck, "get_loop"))
        deckdata.Pitch = self.to_float(await self._get_result(deck, "get_pitch"))
        deckdata.IsPlaying = self.to_bool(await self._get_result(deck, "play"))
        deckdata.IsLooping = self.to_bool(await self._get_result(deck, "loop"))
        deckdata.IsReverse = self.to_bool(await self._get_result(deck, "reverse"))
        deckdata.IsSync = self.to_bool(await self._get_result(deck, "sync"))
        deckdata.IsBeatlock = self.to_bool(await self._get_result(deck, "beatlock"))
        deckdata.IsMasterTempo = self.to_bool(await self._get_result(deck, "master_tempo"))
        deckdata.IsKeylock = self.to_bool(await self._get_result(deck, "key_lock"))
        deckdata.HasStems = self.to_bool(await self._get_result(deck, "has_stems"))
        deckdata.HasLyrics = self.to_bool(await self._get_result(deck, "has_lyrics"))
        deckdata.HasError = self.to_str(await self._get_result(deck, "deck_has_error"))
        deckdata.IsVideo = self.to_bool(await self._get_result(deck, "is_video"))
        deckdata.IsPfl = self.to_bool(await self._get_result(deck, "pfl"))
        deckdata.HasLinkedTracks = self.to_bool(await self._get_result(deck, "has_linked_tracks"))
        return deckdata
    #------------------------------------------------------------------------------------
    #  asyncio.run()
    #------------------------------------------------------------------------------------
    def is_connected(self) -> bool:
        return asyncio.run(self.is_connected_async()) 
    #------------------------------------------------------------------------------------
    def close_app(self, force_close: bool = False) -> bool:
        return asyncio.run(self.close_app_async()) 
    #------------------------------------------------------------------------------------
    def send(self, vdj_script: str) -> bool:
        return asyncio.run(self.send_async(vdj_script))
    #------------------------------------------------------------------------------------
    def get(self, vdj_script: str) -> str:
        return asyncio.run(self.get_async(vdj_script))
    #------------------------------------------------------------------------------------
    def get_loadSecurity(self) -> bool:
        return asyncio.run(self.get_loadSecurity_async())
    #------------------------------------------------------------------------------------
    def disable_loadSecurity(self):
        return asyncio.run(self.disable_loadSecurity_async())
    #------------------------------------------------------------------------------------
    def get_DeckData(self, deck: str) -> VdjDeckData:
        return asyncio.run(self.get_DeckData_async(deck))
   