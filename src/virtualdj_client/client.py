#------------------------------------------------------------------------------------
# VirtualDJ Client
#------------------------------------------------------------------------------------
__version__ = "1.0.28"

import asyncio
import time
from typing import Optional, Literal
from dataclasses import dataclass
from datetime import datetime,timedelta

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
    SongLength: Optional[str] = None   
    TimeTotal: Optional[str] = None  
    HasStems: Optional[bool] = None
    HasStemsV1: Optional[bool] = None
    HasStemsV2: Optional[bool] = None
    HasLyrics: Optional[bool] = None
    HasLinkedTracks: Optional[bool] = None
#------------------------------------------------------------------------------------------------------------------------------------
@dataclass
class VdjDeckEngine:
    HasError: Optional[str] = None
    IsPfl: Optional[bool] = None
    IsPlaying: Optional[bool] = None
    IsAudible: Optional[bool] = None
    IsLooping: Optional[bool] = None
    IsReverse: Optional[bool] = None
    IsSync: Optional[bool] = None
    IsBeatlock: Optional[bool] = None
    IsMasterTempo: Optional[bool] = None
    IsKeylock: Optional[bool] = None
    IsTimecode: Optional[bool] = None
    IsLineIn: Optional[bool] = None
    IsMute: Optional[bool] = None
    IsStemsReady: Optional[bool] = None
    BpmCurrent: Optional[float] = None
    KeyCurrent: Optional[str] = None
    KeyCurrentHarmonic: Optional[str] = None
    Position: Optional[float] = None
    Time: Optional[str] = None
    TimeElapsed: Optional[str] = None
    TimeRemaining: Optional[str] = None
    Beat: Optional[float] = None
    Beatgrid: Optional[float] = None 
    Beatpos: Optional[float] = None
    Firstbeat: Optional[float] = None
    Level: Optional[float] = None
    LoopSize: Optional[int] = None
    Volume: Optional[float] = None
    VolumeTotal: Optional[float] = None
    Pitch: Optional[float] = None
    PitchValue: Optional[float] = None
    Gain: Optional[float] = None
    FilterName: Optional[str] = None
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
    IsInternalMixer: Optional[bool] = None
    Limiter: Optional[float] = None
    IsMic: Optional[bool] = None
    IsMicFx: Optional[bool] = None
    IsMixFx: Optional[bool] = None
    HasSystemVolume: Optional[bool] = None
    Crossfader: Optional[float] = None
    CrossfaderDisable: Optional[bool] = None
    CrossfaderHamster: Optional[bool] = None
    CrossfaderCurve: Optional[str] = None
    CrossfaderCustom: Optional[str] = None
    MasterVolume: Optional[float] = None
    MicVolume:  Optional[float] = None
    Mic2Volume:  Optional[float] = None
    MicFxName: Optional[str] = None
    HeadphoneVolume: Optional[float] = None
    HeadphoneMix: Optional[float] = None
    HeadphoneGain: Optional[float] = None
    HeadphoneCrossfader: Optional[float] = None
    SamplerVolumeMaster: Optional[float] = None
    MasterBalance: Optional[float] = None
    BoothVolume: Optional[float] = None
    MixFxName: Optional[str] = None
    ZeroDB: Optional[str] = None
    SystemVolume: Optional[float] = None
    MasterVuMeterLeft: Optional[float] = None
    MasterVuMeterRight: Optional[float] = None
    EqCrossfaderHigh: Optional[float] = None
    EqCrossfaderMid: Optional[float] = None
    EqCrossfaderLow: Optional[float] = None
#------------------------------------------------------------------------------------------------------------------------------------
@dataclass
class VdjDeckData:
    Song: VdjDeckSong = None
    Engine: VdjDeckEngine = None
#------------------------------------------------------------------------------------------------------------------------------------
@dataclass
class VdjBrowserFolder:
    browsed_folder_tab: Optional[int] = None
    browsed_folder: Optional[str] = None
    browsed_header: Optional[str] = None
    browsed_folder_icon: Optional[int] = None
    browsed_folder_path: Optional[str] = None
    browsed_folder_scrollpos: Optional[int] = None
    browsed_folder_scrollsize: Optional[int] = None
    browsed_folder_selection_index: Optional[int] = None
    file_count: Optional[int] = None
#------------------------------------------------------------------------------------------------------------------------------------
@dataclass
class VdjBrowserFile:
    browsed_title_artist: Optional[str] = None
    browsed_artist: Optional[str] = None
    browsed_title: Optional[str] = None
    browsed_filepath: Optional[str] = None
    browsed_bpm: Optional[float] = None
    browsed_key: Optional[str] = None
    browsed_genre: Optional[str] = None
    browsed_comment: Optional[str] = None
    browsed_composer: Optional[str] = None
    browsed_color: Optional[str] = None
    browsed_album: Optional[str] = None
    browsed_scrollpos: Optional[int] = None
    browsed_scrollsize: Optional[int] = None
    browsed_selection_index: Optional[int] = None
#------------------------------------------------------------------------------------------------------------------------------------
@dataclass
class VdjBrowser:
    Folder: Optional[VdjBrowserFolder] = None
    File: Optional[VdjBrowserFile] = None
#------------------------------------------------------------------------------------------------------------------------------------
@dataclass
class VdjAutomix:
    IsAutomixing: Optional[bool] = None
    IsAutomixDualDeck: Optional[bool] = None
    playlist_time: Optional[str] = None
    playlist_repeat: Optional[bool] = None
    playlist_randomize: Optional[bool] = None
    automix_crossfader: Optional[float] = None
    automix_position: Optional[int] = None
    automix_song_artist: Optional[str] = None
    automix_song_title: Optional[str] = None
    automix_nextsong_artist: Optional[str] = None
    automix_nextsong_title: Optional[str] = None
    AutomixType: Optional[str] = None
    AutomixLength: Optional[str] = None
    repeat_song: Optional[bool] = None
    automixSkipLength: Optional[float] = None
    automixMaxLength: Optional[int] = None
    automixAutoRemovePlayed: Optional[str] = None
    automixTempoMode: Optional[str] = None
    automixBeatMatchOnFade: Optional[bool] = None
    automixDoubleClick: Optional[str] = None
#------------------------------------------------------------------------------------------------------------------------------------
@dataclass
class VdjVideo:
    IsVideoActive: Optional[bool] = None
    video_crossfader: Optional[float] = None
    video_crossfader_link: Optional[bool] = None
    video_crossfader_auto: Optional[bool] = None
    video_fadetoblack: Optional[bool] = None
    has_video_mix: Optional[bool] = None
    video_transition_name: Optional[str] = None
    video_fx_name: Optional[str] = None
#------------------------------------------------------------------------------------------------------------------------------------
class VirtualDJClient():
    def __init__(self):
        self.vdj_client = VirtualDJClientHttp()
        self.vdj_utils = VirtualDJUtils()
        self.vdj_settings = VirtualDJSettings()
    #------------------------------------------------------------------------------------
    async def __aenter__(self):
        return self
    #------------------------------------------------------------------------------------
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
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
            self.vdj_utils.save_client_log(f"VirtualDJ checkUpdates option => {checkUpdates}")
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
            self.vdj_utils.save_client_log("VirtualDJ => loadSecurity option is activated")
        else:
            self.vdj_utils.save_client_log("VirtualDJ => loadSecurity option is disable")

        if is_vdj_security and force_close:
            result = await self.set_loadSecurity_async("off")
            if result == True:
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
    def _to_milliseconds(value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        try:
            sec = float(value)
            ms = int(sec * 1000)
            return str(ms)
        except ValueError:
            return None
    #------------------------------------------------------------------------------------
    @staticmethod
    def _to_strtime(value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        try:
            milliseconds = int(value)
            time = timedelta(milliseconds=milliseconds)
            return str(time)
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
    @staticmethod
    def to_AutomixType(value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        if value == "smart":
            return "Smart"
        elif value == "force fade":
            return "Fade (remove intro/outro)"
        elif value == "skip silence":
            return "Fade (remove silence)"
        elif value == "full songs":
            return "Fade (remove nothing)"
        elif value == "radio":
            return "Fade out, Cut in (remove silence)"
        elif value == "no mix":
            return "None (back-to-back)"
    #------------------------------------------------------------------------------------
    @staticmethod
    def to_AutomixLength(value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        try:
            val = int(value)
            if val < 0:
                return str(abs(val)) + "s gap"
            else:
                return str(val) + "s"
        except ValueError:
            return None
    #------------------------------------------------------------------------------------
    #  Get_Result / Get_Result_Deck
    #------------------------------------------------------------------------------------  
    async def _get_result(self, vdjscript: str) -> str:
        result = await self.get_async(vdjscript)
        result_check = result[0:5]
        if result_check == 'error':
            return None
        return result
    #------------------------------------------------------------------------------------
    async def _get_result_deck(self, deck: str, verb: str) -> str:
        vdjscript = f"deck {deck} {verb}"
        result = await self.get_async(vdjscript)
        result_check = result[0:5]
        if result_check == 'error':
            return None
        return result
    #------------------------------------------------------------------------------------
    #  Deck
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
        song.SongLength = self._to_strtime(self._to_milliseconds(await self._get_result_deck(deck, "get_songlength")))
        song.TimeTotal = self._to_strtime(await self._get_result_deck(deck, "get_time total absolute"))
        song.HasStems = self.to_bool(await self._get_result_deck(deck, "has_stems"))
        song.HasLyrics = self.to_bool(await self._get_result_deck(deck, "has_lyrics"))
        song.HasLinkedTracks = self.to_bool(await self._get_result_deck(deck, "has_linked_tracks"))
        song.IsVideo = self.to_bool(await self._get_result_deck(deck, "is_video"))
        song.HasStemsV1 = self.to_bool(await self._get_result_deck(deck, "has_stems '1.0'"))
        song.HasStemsV2 = self.to_bool(await self._get_result_deck(deck, "has_stems '2.0'"))
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
        deckengine.Time = self._to_strtime(await self._get_result_deck(deck, "get_time"))
        deckengine.TimeElapsed = self._to_strtime(await self._get_result_deck(deck, "get_time elapsed absolute"))
        deckengine.TimeRemaining = self._to_strtime(await self._get_result_deck(deck, "get_time remaining absolute"))
        deckengine.Beat = self.to_float(await self._get_result_deck(deck, "get_beat"))
        deckengine.Beatgrid = self.to_float(await self._get_result_deck(deck, "get_beatgrid"))
        deckengine.Beatpos = self.to_float(await self._get_result_deck(deck, "get_beatpos"))
        deckengine.Firstbeat = self.to_float(await self._get_result_deck(deck, "get_firstbeat"))
        deckengine.Volume = self.to_float(await self._get_result_deck(deck, "volume"))
        deckengine.VolumeTotal = self.to_float(await self._get_result_deck(deck, "get_volume"))
        deckengine.Level = self.to_float(await self._get_result_deck(deck, "get_level"))
        deckengine.LoopSize = self.to_int(await self._get_result_deck(deck, "get_loop"))
        deckengine.Pitch = self.to_float(await self._get_result_deck(deck, "get_pitch"))
        deckengine.PitchValue = self.to_float(await self._get_result_deck(deck, "get_pitch_value"))
        deckengine.IsPlaying = self.to_bool(await self._get_result_deck(deck, "play"))
        deckengine.IsAudible = self.to_bool(await self._get_result_deck(deck, "is_audible"))
        deckengine.IsLooping = self.to_bool(await self._get_result_deck(deck, "loop"))
        deckengine.IsReverse = self.to_bool(await self._get_result_deck(deck, "reverse"))
        deckengine.IsSync = self.to_bool(await self._get_result_deck(deck, "sync"))
        deckengine.IsBeatlock = self.to_bool(await self._get_result_deck(deck, "beatlock"))
        deckengine.IsMasterTempo = self.to_bool(await self._get_result_deck(deck, "master_tempo"))
        deckengine.IsKeylock = self.to_bool(await self._get_result_deck(deck, "key_lock"))
        deckengine.IsTimecode = self.to_bool(await self._get_result_deck(deck, "timecode_active"))
        deckengine.IsLineIn = self.to_bool(await self._get_result_deck(deck, "linein"))
        deckengine.IsMute = self.to_bool(await self._get_result_deck(deck, "mute"))
        deckengine.Gain = self.to_float(await self._get_result_deck(deck, "gain"))
        deckengine.EqHigh = self.to_float(await self._get_result_deck(deck, "eq_high"))
        deckengine.EqMid = self.to_float(await self._get_result_deck(deck, "eq_mid"))
        deckengine.EqLow = self.to_float(await self._get_result_deck(deck, "eq_low"))
        deckengine.EqKillHigh = self.to_bool(await self._get_result_deck(deck, "eq_kill_high"))
        deckengine.EqKillMid = self.to_bool(await self._get_result_deck(deck, "eq_kill_mid")) 
        deckengine.EqKillLow = self.to_bool(await self._get_result_deck(deck, "eq_kill_low"))
        deckengine.FilterName = self.to_str(await self._get_result_deck(deck, "filter_selectcolorfx"))
        deckengine.Filter = self.to_float(await self._get_result_deck(deck, "filter"))
        deckengine.IsStemsReady = self.to_bool(await self._get_result_deck(deck, "has_stems 'ready'"))
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
    async def get_Mixer_async(self) -> VdjMixer:
        # TODO: check if we can use asyncio.gather() to decrease the latency
        mixer = VdjMixer()
        limiter = await self._get_result("get_limiter")
        mixer.Limiter = self.to_float(await self._get_result("get_limiter"))
        mixer.IsMic = self.to_bool(await self._get_result("mic"))
        mixer.IsMicFx = self.to_bool(await self._get_result("effect_active 'mic'"))
        mixer.IsMixFx = self.to_bool(await self._get_result("effect_mixfx_activate"))
        mixer.IsInternalMixer = self.to_bool(await self._get_result("mixermode"))
        mixer.HasSystemVolume = self.to_bool(await self._get_result("has_system_volume"))
        mixer.Crossfader = self.to_float(await self._get_result("crossfader"))
        mixer.CrossfaderDisable = self.to_bool(await self._get_result("crossfader_disable"))
        mixer.CrossfaderHamster = self.to_bool(await self._get_result("crossfader_hamster"))
        mixer.CrossfaderCurve = self.to_crossfaderCurve(await self._get_result("setting 'crossfaderCurve'"))
        mixer.CrossfaderCustom = self.to_str(await self._get_result("setting 'crossfaderCustom'"))
        mixer.MasterVolume = self.to_float(await self._get_result("master_volume"))
        mixer.MicVolume = self.to_float(await self._get_result("mic_volume"))
        mixer.Mic2Volume = self.to_float(await self._get_result("mic2_volume"))
        mixer.HeadphoneVolume = self.to_float(await self._get_result("headphone_volume"))
        mixer.HeadphoneMix = self.to_float(await self._get_result("headphone_mix"))
        mixer.HeadphoneGain = self.to_float(await self._get_result("headphone_gain"))
        mixer.HeadphoneCrossfader = self.to_float(await self._get_result("headphone_crossfader"))
        mixer.SamplerVolumeMaster = self.to_float(await self._get_result("sampler_volume_master"))
        mixer.MasterBalance = self.to_float(await self._get_result("master_balance"))
        mixer.BoothVolume = self.to_float(await self._get_result("booth_volume"))
        mixer.MixFxName = self.to_str(await self._get_result("get_text `effect_mixfx`"))
        mixer.ZeroDB = self.to_zeroDB(await self._get_result("setting 'zeroDB'"))
        mixer.SystemVolume = self.to_float(await self._get_result("system_volume"))
        mixer.MasterVuMeterLeft = self.to_float(await self._get_result("get_vu_meter_left 'master'"))
        mixer.MasterVuMeterRight = self.to_float(await self._get_result("get_vu_meter_right 'master'"))
        mixer.EqCrossfaderHigh = self.to_float(await self._get_result("eq_crossfader_high"))
        mixer.EqCrossfaderMid = self.to_float(await self._get_result("eq_crossfader_mid"))
        mixer.EqCrossfaderLow = self.to_float(await self._get_result("eq_crossfader_low"))
        mixer.MicFxName = self.to_str(await self._get_result("get_effect_name 'mic'"))
        return mixer
    #------------------------------------------------------------------------------------
    #  Browser
    #------------------------------------------------------------------------------------  
    async def get_BrowserFolder_async(self) -> VdjBrowserFolder:
        # TODO: check if we can use asyncio.gather() to decrease the latency
        browserfolder = VdjBrowserFolder()
        browserfolder.browsed_folder = self.to_str(await self._get_result("get_browsed_folder"))
        browserfolder.browsed_folder_icon = self.to_int(await self._get_result("get_browsed_folder_icon"))
        browserfolder.browsed_folder_path = self.to_str(await self._get_result("get_browsed_folder_path"))
        browserfolder.browsed_folder_scrollpos = self.to_int(await self._get_result("get_browsed_folder_scrollpos"))
        browserfolder.browsed_folder_scrollsize = self.to_int(await self._get_result("get_browsed_folder_scrollsize"))
        browserfolder.browsed_folder_selection_index = self.to_int(await self._get_result("get_browsed_folder_selection_index"))
        browserfolder.browsed_folder_tab = self.to_int(await self._get_result("get_browsed_folder_tab"))
        browserfolder.browsed_header = self.to_str(await self._get_result("get_browsed_header"))
        browserfolder.file_count = self.to_int(await self._get_result("file_count"))
        return browserfolder
    #------------------------------------------------------------------------------------
    async def get_BrowserFile_async(self) -> VdjBrowserFile:
        # TODO: check if we can use asyncio.gather() to decrease the latency
        browserfile = VdjBrowserFile()
        browserfile.browsed_scrollpos = self.to_int(await self._get_result("get_browsed_scrollpos"))
        browserfile.browsed_scrollsize = self.to_int(await self._get_result("get_browsed_scrollsize"))
        browserfile.browsed_selection_index = self.to_int(await self._get_result("get_browsed_selection_index"))
        browserfile.browsed_filepath = self.to_str(await self._get_result("get_browsed_filepath"))
        browserfile.browsed_artist = self.to_str(await self._get_result("get_browsed_artist"))
        browserfile.browsed_title = self.to_str(await self._get_result("get_browsed_title"))
        browserfile.browsed_title_artist = self.to_str(await self._get_result("get_browsed_title_artist "))
        browserfile.browsed_bpm = self.to_float(await self._get_result("get_browsed_bpm"))
        browserfile.browsed_key = self.to_str(await self._get_result("get_browsed_key"))
        browserfile.browsed_genre = self.to_str(await self._get_result("get_browsed_genre"))
        browserfile.browsed_comment = self.to_str(await self._get_result("get_browsed_comment"))
        browserfile.browsed_composer = self.to_str(await self._get_result("get_browsed_composer"))
        browserfile.browsed_color = self.to_str(await self._get_result("get_browsed_color"))
        browserfile.browsed_album = self.to_str(await self._get_result("get_browsed_album"))
        return browserfile
    #------------------------------------------------------------------------------------
    async def get_Browser_async(self) -> VdjBrowser:
        browser = VdjBrowser()
        browser.Folder = await self.get_BrowserFolder_async()
        browser.File = await self.get_BrowserFile_async()
        return browser
    #------------------------------------------------------------------------------------
    #  Automix
    #------------------------------------------------------------------------------------ 
    async def get_Automix_async(self) -> VdjAutomix:
        # TODO: check if we can use asyncio.gather() to decrease the latency
        automix = VdjAutomix()
        automix.IsAutomixing = self.to_bool(await self._get_result("automix"))
        automix.IsAutomixDualDeck = self.to_bool(await self._get_result("automix_dualdeck"))
        automix.playlist_time = self.to_str(await self._get_result("get_playlist_time"))
        automix.playlist_repeat = self.to_bool(await self._get_result("playlist_repeat"))
        automix.playlist_randomize = self.to_bool(await self._get_result("playlist_randomize"))
        automix.automix_crossfader = self.to_float(await self._get_result("get_automix"))
        automix.automix_position = self.to_int(await self._get_result("get_automix_position"))
        automix.automix_song_artist = self.to_str(await self._get_result("get_automix_song 'artist' 0"))
        automix.automix_song_title = self.to_str(await self._get_result("get_automix_song 'title' 0"))
        automix.automix_nextsong_artist = self.to_str(await self._get_result("get_automix_song 'artist' 1"))
        automix.automix_nextsong_title = self.to_str(await self._get_result("get_automix_song 'title' 1"))
        automix.AutomixType = self.to_AutomixType(await self._get_result("setting 'automixMode'"))
        automix.AutomixLength = self.to_AutomixLength(await self._get_result("setting 'fadeLength'"))
        automix.repeat_song = self.to_bool(await self._get_result("repeat_song"))
        automix.automixSkipLength = self.to_float(await self._get_result("setting 'automixSkipLength'"))
        automix.automixMaxLength = self.to_int(await self._get_result("setting 'automixMaxLength'"))
        automix.automixAutoRemovePlayed = self.to_str(await self._get_result("setting 'automixAutoRemovePlayed'"))
        automix.automixTempoMode = self.to_str(await self._get_result("setting 'automixTempoMode'"))
        automix.automixBeatMatchOnFade = self.to_bool(await self._get_result("setting 'autoMixBeatMatchOnFade'"))
        automix.automixDoubleClick = self.to_str(await self._get_result("setting 'automixDoubleClick'"))
        return automix
    #------------------------------------------------------------------------------------
    #  Video
    #------------------------------------------------------------------------------------ 
    async def get_Video_async(self) -> VdjVideo:
        # TODO: check if we can use asyncio.gather() to decrease the latency
        video = VdjVideo()
        video.IsVideoActive = self.to_bool(await self._get_result("video"))
        video.video_crossfader = self.to_float(await self._get_result("video_crossfader"))
        video.video_crossfader_link = self.to_bool(await self._get_result("video_crossfader_link"))
        video.video_crossfader_auto = self.to_bool(await self._get_result("video_crossfader_auto"))
        video.video_fadetoblack = self.to_bool(await self._get_result("video_fadetoblack"))
        video.has_video_mix = self.to_bool(await self._get_result("has_video_mix"))
        video.video_transition_name = self.to_str(await self._get_result("get_videotrans_name"))
        video.video_fx_name = self.to_str(await self._get_result("get_videofx_name"))
        return video
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
    #------------------------------------------------------------------------------------
    def get_BrowserFolder(self) -> VdjBrowserFolder:
        return asyncio.run(self.get_BrowserFolder_async())
    #------------------------------------------------------------------------------------
    def get_BrowserFile(self) -> VdjBrowserFile:
        return asyncio.run(self.get_BrowserFile_async())
    #------------------------------------------------------------------------------------
    def get_Browser(self) -> VdjBrowser:
        return asyncio.run(self.get_Browser_async())
    #------------------------------------------------------------------------------------
    def get_Automix(self) -> VdjAutomix:
        return asyncio.run(self.get_Automix_async())
    #------------------------------------------------------------------------------------
    def get_Video(self) -> VdjVideo:
        return asyncio.run(self.get_Video_async())