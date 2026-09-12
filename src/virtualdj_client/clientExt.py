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
    Artist: Optional[str] = None
    Title: Optional[str] = None
    Remix: Optional[str] = None
    Bpm: Optional[int] = None
    Key: Optional[str] = None
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
    #------------------------------------------------------------------------------------------------------------------------------------
    async def get_DeckData_async(self, deck: str) -> VdjDeckData:
        deckdata = VdjDeckData()
        deckdata.Bpm = await self._get_result(deck, "get_bpm")
        deckdata.Key = await self._get_result(deck, "get_key")
        return deckdata
    #------------------------------------------------------------------------------------------------------------------------------------
    def get_DeckData(self, deck: str) -> VdjDeckData:
        return asyncio.run(self.get_DeckData_async(deck))


