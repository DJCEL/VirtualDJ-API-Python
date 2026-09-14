#------------------------------------------------------------------------------------
# VirtualDJ Client
#------------------------------------------------------------------------------------
__version__ = "1.0.24"

import asyncio
import time
from typing import Optional, Literal
from dataclasses import dataclass

from .client_http import VirtualDJClientHttp, VdjResponse
from .client_utils import VirtualDJUtils
from .client_settings import VirtualDJSettings, VdjSettings

#------------------------------------------------------------------------------------------------------------------------------------
@dataclass
class VdjDeck:
    name: Literal['left', 'right', 'leftvideo', 'rightvideo', 'all', 'default', 'active', 'master'] | None = None
    id: int | None = None
#------------------------------------------------------------------------------------------------------------------------------------
@dataclass
class VdjDeckSong:
    Filepath: Optional[str] = None
    Filesize: Optional[int] = None
    IsVideo: Optional[bool] = None
    Artist: Optional[str] = None
    Title: Optional[str] = None
    Remix: Optional[str] = None
    Album: Optional[str] = None
    Genre: Optional[str] = None
    Year: Optional[int] = None
    Rating: Optional[int] = None
    Comment: Optional[str] = None
    Bpm: Optional[float] = None    
    Key: Optional[str] = None
    KeyHarmonic: Optional[str] = None
    Duration: Optional[float] = None   
    HasStems: Optional[bool] = None
    HasLyrics: Optional[bool] = None
    HasLinkedTracks: Optional[bool] = None
#------------------------------------------------------------------------------------------------------------------------------------
@dataclass
class VdjDeckEngine:
    HasError: Optional[str] = None
    IsPfl: Optional[bool] = None
    IsPlaying: Optional[bool] = None
    IsLooping: Optional[bool] = None
    IsReverse: Optional[bool] = None
    IsSync: Optional[bool] = None
    IsBeatlock: Optional[bool] = None
    IsMasterTempo: Optional[bool] = None
    IsKeylock: Optional[bool] = None
    IsTimecode: Optional[bool] = None
    BpmCurrent: Optional[float] = None
    KeyCurrent: Optional[str] = None
    KeyCurrentHarmonic: Optional[str] = None
    Position: Optional[float] = None
    Time: Optional[float] = None
    Beat: Optional[float] = None
    Beatgrid: Optional[float] = None 
    Beatpos: Optional[float] = None
    Firstbeat: Optional[float] = None
    Level: Optional[float] = None
    LoopSize: Optional[int] = None
    Volume: Optional[float] = None
    VolumeTotal: Optional[float] = None
    Pitch: Optional[float] = None
    Gain: Optional[float] = None
    Filter: Optional[float] = None
    EqHigh: Optional[float] = None
    EqMid: Optional[float] = None
    EqLow: Optional[float] = None
    EqKillHigh: Optional[bool] = None
    EqKillMid: Optional[bool] = None
    EqKillLow: Optional[bool] = None
#------------------------------------------------------------------------------------------------------------------------------------
@dataclass
class VdjMixer:
    IsLimiterRunning: Optional[bool] = None
    IsMic: Optional[bool] = None
    IsMixFx: Optional[bool] = None
    Crossfader: Optional[float] = None
    CrossfaderDisable: Optional[bool] = None
    CrossfaderHamster: Optional[bool] = None
    CrossfaderCurve: Optional[str] = None
    CrossfaderCustom: Optional[str] = None
    MasterVolume: Optional[float] = None
    MicVolume:  Optional[float] = None
    HeadphoneVolume: Optional[float] = None
    HeadphoneMix: Optional[float] = None
    HeadphoneGain: Optional[float] = None
    HeadphoneCrossfader: Optional[float] = None
    SamplerVolumeMaster: Optional[float] = None
    MasterBalance: Optional[float] = None
    BoothVolume: Optional[float] = None
    MixFx: Optional[str] = None
    ZeroDB: Optional[str] = None
#------------------------------------------------------------------------------------------------------------------------------------
@dataclass
class VdjDeckData:
    Song: VdjDeckSong = None
    Engine: VdjDeckEngine = None
#------------------------------------------------------------------------------------------------------------------------------------
@dataclass
class VdjDeckCache:
    data: VdjDeckData | None = None
    updated_at: float = 0.0
#------------------------------------------------------------------------------------------------------------------------------------
class VirtualDJClient():
    def __init__(self):
        self.vdj_client = VirtualDJClientHttp()
        self.vdj_utils = VirtualDJUtils()
        self.vdj_settings = VirtualDJSettings()
        self._deck_cache: dict[str,VdjDeckData] = {}
        self._refresh_task: asyncio.Task | None = None
        self._refresh_interval = 1.0
    #------------------------------------------------------------------------------------
    #  Check if VirtualDJ is connected
    #------------------------------------------------------------------------------------
    async def is_connected_async(self) -> bool:
        """ 
        Check if Network Control Plugin is responding 
        """
        vdj_response = await self.vdj_client.query("get_version")
        status = vdj_response.status
        status_code = vdj_response.status_code
        result = vdj_response.result
        self.vdj_utils.save_client_log(f"HTTP {status_code}: {status} / {result}")
        if status == "ok":
           return True
        else:
            return False
    #------------------------------------------------------------------------------------
    #  Launch / Quit VirtualDJ
    #------------------------------------------------------------------------------------
    def is_app_running(self) -> bool:
        """ 
        Check if VirtualDJ software is running 
        """
        return self.vdj_utils.is_virtualdj_running()
    #------------------------------------------------------------------------------------
    def get_checkUpdates(self) -> bool:
        """ 
        Check if checkUpdates is activated in VirtualDJ settings
        """
        bRes = False
        settings: VdjSettings = None
        settings_path_list = self.vdj_settings.get_local_settings_path_list()
        for settings_path in settings_path_list:
            settings = self.vdj_settings.read_local_xml_settings(settings_path)
            checkUpdates = settings.internet.checkUpdates
            if checkUpdates.lower() in ['yes','yes (silent)']:
                bRes = True
        return bRes
    #------------------------------------------------------------------------------------
    def set_checkUpdates(self, value:str) -> bool:
        """ 
        set checkUpdates in VirtualDJ settings
        """
        #TODO: write the new value in VirtualDJ settings
        return False
    #------------------------------------------------------------------------------------
    def open_app(self) -> bool:
        """ 
        Open VirtuaDJ if not open 
        """
        is_vdj_running = self.is_app_running()
        if is_vdj_running == True:
            return True

        checkUpdates = self.get_checkUpdates()
        if checkUpdates:
            print(f"VirtualDJ checkUpdates option => {checkUpdates}")
            self.set_checkUpdates('off')

        bRes = self.vdj_utils.launch_virtualdj_software()
        return bRes 
    #------------------------------------------------------------------------------------
    async def get_loadSecurity_async(self) -> bool:
        """ 
        Get the loadSecurity option
        """
        vdjscript = 'setting "loadSecurity"'
        result = await self.get_async(vdjscript)
        if result in ['on','silent']:
           return True
        else:
           return False    
    #------------------------------------------------------------------------------------
    async def set_loadSecurity_async(self, value: str) -> bool:
        """ 
        Set the loadSecurity option
        """
        vdjscript = f'setting "loadSecurity" {value}'
        result = await self.send_async(vdjscript)
        return result
    #------------------------------------------------------------------------------------
    async def close_app_async(self, force_close: bool = False) -> bool:
        """ 
        Close VirtuaDJ 
        """
        is_vdj_running = self.is_app_running()
        if is_vdj_running == False:
            return True

        is_vdj_security = await self.get_loadSecurity_async()
        if is_vdj_security:
            print("VirtualDJ => loadSecurity option is activated")
            self.vdj_utils.save_client_log("VirtualDJ => loadSecurity option is activated")
        else:
            print("VirtualDJ => loadSecurity option is disable")
            self.vdj_utils.save_client_log("VirtualDJ => loadSecurity option is disable")

        if is_vdj_security and force_close:
            result = await self.set_loadSecurity_async("off")
            if result == True:
                print("VirtualDJ => loadSecurity option is now disable")
                self.vdj_utils.save_client_log("VirtualDJ => loadSecurity option is now disable")


        close = await self.send_async("close")
        if close == True:
            return True

        # TODO: Force kill app if (force_close == True)
        return False
    #------------------------------------------------------------------------------------
    #  VirtualDJ Get/Send
    #------------------------------------------------------------------------------------
    async def get_async(self, vdjscript: str) -> str:
        """ 
        Query VirtualDJ with a vdjscript 
        """
        vdj_response = await self.vdj_client.query(vdjscript)
        status = vdj_response.status
        status_code = vdj_response.status_code
        result = vdj_response.result
        self.vdj_utils.save_client_log(f"HTTP {status_code}: {status} / {result}")
        if status == "ok": 
            return result
        else:
            return result           
    #------------------------------------------------------------------------------------
    async def send_async(self, vdjscript: str) -> bool:
        """ Execute a vdjscript and return status """
        vdj_response = await self.vdj_client.execute(vdjscript)
        status = vdj_response.status
        status_code = vdj_response.status_code
        result = vdj_response.result
        self.vdj_utils.save_client_log(f"HTTP {status_code}: {status} / {result}")
        if status == "ok":
            return (result.lower() == "true")
        else:
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
    @staticmethod
    def to_crossfaderCurve(value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        try:
            val = float(value)
            if val == 0.5:
                return 'Full'
            elif val == 0.33:
                return 'Smooth'
            elif val == 0.99:
                return 'Scratch'
            elif val == -1:
                return 'Cut'
            elif val == -2:
                return 'Custom'
            else:
                return value
        except ValueError:
            return None
    #------------------------------------------------------------------------------------
    @staticmethod
    def to_zeroDB(value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        try:
            val = float(value)
            if val == 1:
                return 'Default'
            elif val == 0.89:
                return '-1dB'
            elif val == 0.71:
                return '-3dB'
            elif val == 0.5:
                return '-6dB'
            elif val == 0.35:
                return '-9dB'
            elif val == 0.25:
                return '-12dB'
            else:
                return value
        except ValueError:
            return None
    #------------------------------------------------------------------------------------
    #  Deck
    #------------------------------------------------------------------------------------  
    async def _get_result_deck(self, deck: str, verb: str) -> str:
        vdjscript = f"deck {deck} {verb}"
        result = await self.get_async(vdjscript)
        result_check = result[0:5]
        if result_check == 'error':
            return None
        return result
    #------------------------------------------------------------------------------------
    async def get_DeckSong_async(self, deck: str) -> VdjDeckSong:
        # TODO: check if we can use asyncio.gather() to decrease the latency
        song = VdjDeckSong()
        song.Filepath = self.to_str(await self._get_result_deck(deck, "get_filepath"))
        song.Filesize = self.to_int(await self._get_result_deck(deck, "get_filesize"))
        song.Artist = self.to_str(await self._get_result_deck(deck, "get_artist"))
        song.Title = self.to_str(await self._get_result_deck(deck, "get_title"))
        song.Remix = self.to_str(await self._get_result_deck(deck, "get_remix"))
        song.Genre = self.to_str(await self._get_result_deck(deck, "get_genre"))
        song.Album = self.to_str(await self._get_result_deck(deck, "get_album"))
        year_tmp = self.to_int(await self._get_result_deck(deck, "get_year"))
        song.Year = None if year_tmp == 0 else year_tmp
        song.Rating = self.to_int(await self._get_result_deck(deck, "rating"))
        song.Comment = self.to_str(await self._get_result_deck(deck, "get_comment"))
        song.Bpm = self.to_float(await self._get_result_deck(deck, "get_bpm absolute"))
        song.Duration = self.to_float(await self._get_result_deck(deck, "get_songlength"))     
        song.HasStems = self.to_bool(await self._get_result_deck(deck, "has_stems"))
        song.HasLyrics = self.to_bool(await self._get_result_deck(deck, "has_lyrics"))
        song.HasLinkedTracks = self.to_bool(await self._get_result_deck(deck, "has_linked_tracks"))
        song.IsVideo = self.to_bool(await self._get_result_deck(deck, "is_video"))
        return song
    #------------------------------------------------------------------------------------
    async def get_DeckEngine_async(self, deck: str) -> VdjDeckEngine:
        # TODO: check if we can use asyncio.gather() to decrease the latency
        deckengine = VdjDeckEngine()
        deckengine.HasError = self.to_str(await self._get_result_deck(deck, "deck_has_error"))
        deckengine.IsPfl = self.to_bool(await self._get_result_deck(deck, "pfl"))
        deckengine.BpmCurrent = self.to_float(await self._get_result_deck(deck, "get_bpm"))
        deckengine.KeyCurrent = self.to_str(await self._get_result_deck(deck, "get_key 'musical'"))
        deckengine.KeyCurrentHarmonic = self.to_str(await self._get_result_deck(deck, "get_harmonic"))
        deckengine.Position = self.to_float(await self._get_result_deck(deck, "get_position"))
        deckengine.Time = self.to_float(await self._get_result_deck(deck, "get_time"))
        deckengine.Beat = self.to_float(await self._get_result_deck(deck, "get_beat"))
        deckengine.Beatgrid = self.to_float(await self._get_result_deck(deck, "get_beatgrid"))
        deckengine.Beatpos = self.to_float(await self._get_result_deck(deck, "get_beatpos"))
        deckengine.Firstbeat = self.to_float(await self._get_result_deck(deck, "get_firstbeat"))
        deckengine.Volume = self.to_float(await self._get_result_deck(deck, "volume"))
        deckengine.VolumeTotal = self.to_float(await self._get_result_deck(deck, "get_volume"))
        deckengine.Level = self.to_float(await self._get_result_deck(deck, "get_level"))
        deckengine.LoopSize = self.to_int(await self._get_result_deck(deck, "get_loop"))
        deckengine.Pitch = self.to_float(await self._get_result_deck(deck, "get_pitch"))
        deckengine.IsPlaying = self.to_bool(await self._get_result_deck(deck, "play"))
        deckengine.IsLooping = self.to_bool(await self._get_result_deck(deck, "loop"))
        deckengine.IsReverse = self.to_bool(await self._get_result_deck(deck, "reverse"))
        deckengine.IsSync = self.to_bool(await self._get_result_deck(deck, "sync"))
        deckengine.IsBeatlock = self.to_bool(await self._get_result_deck(deck, "beatlock"))
        deckengine.IsMasterTempo = self.to_bool(await self._get_result_deck(deck, "master_tempo"))
        deckengine.IsKeylock = self.to_bool(await self._get_result_deck(deck, "key_lock"))
        deckengine.IsTimecode = self.to_bool(await self._get_result_deck(deck, "timecode_active"))
        deckengine.Gain = self.to_float(await self._get_result_deck(deck, "gain"))
        deckengine.EqHigh = self.to_float(await self._get_result_deck(deck, "eq_low"))
        deckengine.EqMid = self.to_float(await self._get_result_deck(deck, "eq_low"))
        deckengine.EqLow = self.to_float(await self._get_result_deck(deck, "eq_low"))
        deckengine.EqKillHigh = self.to_bool(await self._get_result_deck(deck, "eq_kill_high"))
        deckengine.EqKillMid = self.to_bool(await self._get_result_deck(deck, "eq_kill_mid")) 
        deckengine.EqKillLow = self.to_bool(await self._get_result_deck(deck, "eq_kill_low"))
        deckengine.Filter = self.to_float(await self._get_result_deck(deck, "filter"))
        return deckengine
    #------------------------------------------------------------------------------------
    async def get_DeckData_async(self, deck: str) -> VdjDeckData:
        deckdata = VdjDeckData()
        deckdata.Song = await self.get_DeckSong_async(deck)
        deckdata.Engine = await self.get_DeckEngine_async(deck)
        return deckdata
    #------------------------------------------------------------------------------------
    #  Mixer
    #------------------------------------------------------------------------------------  
    async def _get_result_mixer(self, vdjscript: str) -> str:
        result = await self.get_async(vdjscript)
        result_check = result[0:5]
        if result_check == 'error':
            return None
        return result
    #------------------------------------------------------------------------------------
    async def get_Mixer_async(self) -> VdjMixer:
        # TODO: check if we can use asyncio.gather() to decrease the latency
        mixer = VdjMixer()
        mixer.IsLimiterRunning = self.to_bool(await self._get_result_mixer("get_limiter"))
        mixer.IsMic = self.to_bool(await self._get_result_mixer("mic"))
        mixer.IsMixFx = self.to_bool(await self._get_result_mixer("effect_mixfx_activate"))
        mixer.Crossfader = self.to_float(await self._get_result_mixer("crossfader"))
        mixer.CrossfaderDisable = self.to_bool(await self._get_result_mixer("crossfader_disable"))
        mixer.CrossfaderHamster = self.to_bool(await self._get_result_mixer("crossfader_hamster"))
        mixer.CrossfaderCurve = self.to_crossfaderCurve(await self._get_result_mixer("setting 'crossfaderCurve'"))
        mixer.CrossfaderCustom = self.to_str(await self._get_result_mixer("setting 'crossfaderCustom'"))
        mixer.MasterVolume = self.to_float(await self._get_result_mixer("master_volume"))
        mixer.MicVolume = self.to_float(await self._get_result_mixer("mic_volume"))
        mixer.HeadphoneVolume = self.to_float(await self._get_result_mixer("headphone_volume"))
        mixer.HeadphoneMix = self.to_float(await self._get_result_mixer("headphone_mix"))
        mixer.HeadphoneGain = self.to_float(await self._get_result_mixer("headphone_gain"))
        mixer.HeadphoneCrossfader = self.to_float(await self._get_result_mixer("headphone_crossfader"))
        mixer.SamplerVolumeMaster = self.to_float(await self._get_result_mixer("sampler_volume_master"))
        mixer.MasterBalance = self.to_float(await self._get_result_mixer("master_balance"))
        mixer.BoothVolume = self.to_float(await self._get_result_mixer("booth_volume"))
        mixer.MixFx = self.to_str(await self._get_result_mixer("setting 'mixfx'"))
        mixer.ZeroDB = self.to_zeroDB(await self._get_result_mixer("setting 'zeroDB'"))
        return mixer    
    #------------------------------------------------------------------------------------
    #  Refresh loop task
    #------------------------------------------------------------------------------------ 
    async def start_refresh_async(self):
        if self._refresh_task is None or self._refresh_task.done():
            self._refresh_task = asyncio.create_task(self._refresh_loop_async(), name="virtualdj-refresh-loop")
    #------------------------------------------------------------------------------------
    async def stop_refresh_async(self):
         if self._refresh_task is not None:
             self._refresh_task.cancel()

             try:
                 await self._refresh_task
             except asyncio.CancelledError:
                 pass

             self._refresh_task = None
    #------------------------------------------------------------------------------------
    async def _refresh_loop_async(self):
        try:
            while True:
            time_start = time.monotonic()
            try:
               await self._refresh_cache_async()
            except asyncio.CancelledError:
                raise
            except Exception as e:
                self.vdj_utils.save_client_log(f"Refresh loop error: {type(e).__name__}: {e}")

            now = time.monotonic()
            time_elapsed = now - time_start
            delay = max(0.0, self._refresh_interval - time_elapsed)
            await asyncio.sleep(delay)
        finally:
            current_task = asyncio.current_task()
            if self._refresh_task is current_task:
                self._refresh_task = None
    #------------------------------------------------------------------------------------
    async def _refresh_cache_async(self):
        left, right = await asyncio.gather(
            self.get_DeckData_async("left"),
            self.get_DeckData_async("right")
        )

        now = time.monotonic()

        self._deck_cache["left"] = VdjDeckCache(data=left,updated_at=now)
        self._deck_cache["right"] = VdjDeckCache(data=right,updated_at=now)
    #------------------------------------------------------------------------------------
    async def get_DeckData_cached_async(self, deck: str) -> VdjDeckData | None:
        return self._deck_cache.get(deck)
    #------------------------------------------------------------------------------------
    #  asyncio.run()
    #------------------------------------------------------------------------------------
    def is_connected(self) -> bool:
        return asyncio.run(self.is_connected_async()) 
    #------------------------------------------------------------------------------------
    def close_app(self, force_close: bool = False) -> bool:
        return asyncio.run(self.close_app_async(force_close)) 
    #------------------------------------------------------------------------------------
    def send(self, vdjscript: str) -> bool:
        return asyncio.run(self.send_async(vdjscript))
    #------------------------------------------------------------------------------------
    def get(self, vdjscript: str) -> str:
        return asyncio.run(self.get_async(vdjscript))
    #------------------------------------------------------------------------------------
    def get_loadSecurity(self) -> bool:
        return asyncio.run(self.get_loadSecurity_async())
    #------------------------------------------------------------------------------------
    def set_loadSecurity(self, value: str):
        return asyncio.run(self.set_loadSecurity_async(value))
    #------------------------------------------------------------------------------------
    def get_DeckSong(self, deck: str) -> VdjDeckSong:
        return asyncio.run(self.get_DeckSong_async(deck))
    #------------------------------------------------------------------------------------
    def get_DeckEngine(self, deck: str) -> VdjDeckEngine:
        return asyncio.run(self.get_DeckEngine_async(deck))
    #------------------------------------------------------------------------------------
    def get_DeckData(self, deck: str) -> VdjDeckData:
        return asyncio.run(self.get_DeckData_async(deck))
    #------------------------------------------------------------------------------------
    def get_Mixer(self) -> VdjMixer:
        return asyncio.run(self.get_Mixer_async())
