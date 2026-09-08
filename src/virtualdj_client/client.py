""" 
VirtualDJ HTTP API client using the Network Control plugin 
"""
__version__ = '1.0.20'

import httpx
import asyncio
from typing import Optional,Literal
from dataclasses import dataclass
from urllib.parse import quote as encodeURI

from .client_utils import VirtualDJUtils
from .client_config import VDJ_NETWORK_CONTROL_HOST, VDJ_NETWORK_CONTROL_PORT, VDJ_NETWORK_CONTROL_PASSWORD, VDJ_NETWORK_CONTROL_TIMEOUT

#------------------------------------------------------------------------------------------------------------------------------------
@dataclass
class VDJDeck:
    name: Literal['left', 'right', 'leftvideo', 'rightvideo', 'all', 'default', 'active', 'master'] = None
    id: int = None
#------------------------------------------------------------------------------------
@dataclass
class VDJResponse:
    status: Literal["ok","error"]
    status_code: int
    result: str
#------------------------------------------------------------------------------------------------------------------------------------
class VirtualDJClient:
    def __init__(self):
        self.vdj_utils = VirtualDJUtils()
        self.vdj_base_url = f"http://{VDJ_NETWORK_CONTROL_HOST}:{VDJ_NETWORK_CONTROL_PORT}"
        self._client: httpx.AsyncClient | None = None
    #------------------------------------------------------------------------------------
    async def __aenter__(self):
        self._client = httpx.AsyncClient(timeout=VDJ_NETWORK_CONTROL_TIMEOUT)
        return self
    #------------------------------------------------------------------------------------
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()
            self._client = None
    #------------------------------------------------------------------------------------
    def _get_headers(self) -> dict[str, str]:
        headers = {"Content-Type": "text/plain"}
        if VDJ_NETWORK_CONTROL_PASSWORD:
            headers["Authorization"] = f"Bearer {VDJ_NETWORK_CONTROL_PASSWORD}"
        return headers
    #------------------------------------------------------------------------------------
    async def _send_vdj_request(self, vdj_script: str, is_query: bool = False) -> VDJResponse:
        """ Send command via HTTP Network Control plugin """
        vdj_endpoint = "query" if is_query else "execute"
        headers = self._get_headers()
        vdj_url = f"{self.vdj_base_url}/{vdj_endpoint}"
        encoded_vdjscript = encodeURI(vdj_script)
        vdj_url_full = f"{vdj_url}?script={encoded_vdjscript}"

        try:
            if self._client  is None:
                 self._client = httpx.AsyncClient(timeout=VDJ_NETWORK_CONTROL_TIMEOUT)

            response = await self._client.get(vdj_url_full, headers=headers)
            status_code = response.status_code
            if status_code == 200:
                encoding = response.encoding
                content_type =  response.headers["content-type"]
                result = response.text.strip()
                if is_query:
                    result_len = len(result)
                    bErr = False 
                    if (result_len >= 6):
                        ext_result = result[0:6]
                        bErr = (ext_result.lower() == "error:")
                    status = "error" if bErr else "ok"
                    return VDJResponse(status=status, status_code=status_code, result=result)
                else:
                    bErr = (result.lower() != "true")
                    status = "error" if bErr else "ok"
                    return VDJResponse(status=status, status_code=status_code, result=result)
            elif status_code == 401:
                status = "error"
                result = "Authentication failed - check password"
                return VDJResponse(status=status, status_code=status_code, result=result)
            else:
                status = "error"
                result = f"{response.text}"
                return VDJResponse(status=status, status_code=status_code, result=result)

        except httpx.ConnectError:
            status = "error"
            status_code = -1
            result = "HTTP Connection error"
            return VDJResponse(status=status, status_code=status_code, result=result)
        except httpx.TimeoutException:
            status = "error"
            status_code = -2
            result = "HTTP timeout"
            return VDJResponse(status=status, status_code=status_code, result=result)
        except httpx.HTTPError as e:
            status = "error"
            status_code = -3
            result = f"{e} It could be a problem of password too."
            return VDJResponse(status=status, status_code=status_code, result=result)
        except Exception as e:
            status = "error"
            status_code = -4
            result = str(e)
            return VDJResponse(status=status, status_code=status_code, result=result)
    #------------------------------------------------------------------------------------
    async def _query(self, vdj_script: str) -> VDJResponse:
        """ Query VirtualDJ with a vdj_script """
        vdj_response = await self._send_vdj_request(vdj_script, is_query=True)
        return vdj_response
    #------------------------------------------------------------------------------------    
    async def _execute(self, vdj_script: str) -> VDJResponse:
        """ Send command to VirtualDJ with a vdj_script """
        vdj_response = await self._send_vdj_request(vdj_script)
        return vdj_response
    #------------------------------------------------------------------------------------
    async def _query_vdj_script(self, vdj_script: str) -> str:
        """ Query VirtualDJ with a vdj_script """
        vdj_response = await self._query(vdj_script)
        bRes = (vdj_response.status == "ok")
        if bRes:
            result_final = vdj_response.result 
            return result_final
        else:
            status_code = vdj_response.status_code
            result_final = vdj_response.result
            self.vdj_utils.SaveClientLog(f"HTTP error {status_code}: {result_final}")
            return f"Failed to query < {vdj_script} >: {result_final}"            
    #------------------------------------------------------------------------------------
    async def _execute_vdj_script(self, vdj_script: str) -> bool:
        """ Execute a vdj_script and return status """
        vdj_response = await self._execute(vdj_script)
        bRes = (vdj_response.status == "ok")
        if bRes:
            bRes2 = (vdj_response.result.lower() == "true")
            return bRes2
        else:
            status_code = vdj_response.status_code
            result_final = vdj_response.result
            self.vdj_utils.SaveClientLog(f"HTTP error {status_code}: {result_final}")
            return False
    #------------------------------------------------------------------------------------
    async def send_async(self, vdj_script: str) -> bool:
        return await self._execute_vdj_script(vdj_script)
    #------------------------------------------------------------------------------------
    async def get_async(self, vdj_script: str) -> str:
        return await self._query_vdj_script(vdj_script)
    #------------------------------------------------------------------------------------
    def send(self, vdj_script: str) -> bool:
        return asyncio.run(self.send_async(vdj_script))
    #------------------------------------------------------------------------------------
    def get(self, vdj_script: str) -> str:
        return asyncio.run(self.get_async(vdj_script))
    #------------------------------------------------------------------------------------
    # VirtualDJ script tools
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
    #  Launch / Quit VirtualDJ
    #------------------------------------------------------------------------------------
    def is_app_running(self) -> bool:
        """ Check if VirtualDJ software is running """
        return self.vdj_utils.is_virtualdj_running()
    #------------------------------------------------------------------------------------
    def open_app(self) -> bool:
        """ Open VirtuaDJ """
        is_vdj_running = self.is_app_running()
        if is_vdj_running == True:
            return True

        bRes = self.vdj_utils.launch_virtualdj_software()
        return bRes 
    #------------------------------------------------------------------------------------
    async def get_loadSecurity_async(self) -> bool:
        vdj_script = 'setting "loadSecurity"'
        result = await self.get_async(vdj_script)
        if result in ['on','silent']:
           print("VirtualDJ => loadSecurity option is activated")
           self.vdj_utils.SaveClientLog("VirtualDJ => loadSecurity option is activated")
           return True
        else:
           print("VirtualDJ => loadSecurity option is disable")
           self.vdj_utils.SaveClientLog("VirtualDJ => loadSecurity option is disable")
           return False
    #------------------------------------------------------------------------------------
    def get_loadSecurity(self) -> bool:
        return asyncio.run(self.get_loadSecurity_async())
    #------------------------------------------------------------------------------------
    async def disable_loadSecurity_async(self):
        vdj_script = 'setting "loadSecurity" off'
        result = await self.send_async(vdj_script)
        if result == True:
            print("VirtualDJ => loadSecurity option is now disable")
            self.vdj_utils.SaveClientLog("VirtualDJ => loadSecurity option is now disable")
    #------------------------------------------------------------------------------------
    def disable_loadSecurity(self):
        return asyncio.run(self.disable_loadSecurity_async())
    #------------------------------------------------------------------------------------
    def close_app(self, force_close: bool = False) -> bool:
        """ Close VirtuaDJ """
        is_vdj_running = self.is_app_running()
        if is_vdj_running == False:
            return True

        is_vdj_connected = self.is_connected()
        if is_vdj_connected == True:
            is_vdj_security = self.get_loadSecurity()
            if is_vdj_security and force_close:
                self.disable_loadSecurity()

            # Close VirtualDJ
            vdj_script = "close"
            result = self.send(vdj_script)
            if result == True:
                return True

        # TODO: Force kill app if (force_close == True)
        return False
    #------------------------------------------------------------------------------------
    #  Check if VirtualDJ is connected
    #------------------------------------------------------------------------------------
    async def is_connected_async(self) -> bool:
        """ Check if VirtualDJ software is running and Network Control Plugin is responding """
        is_vdj_running = self.is_app_running()
        if is_vdj_running == False:
            return False

        vdj_script = "get_version"
        vdj_response = await self._query(vdj_script)
        bRes = (vdj_response.status == "ok")
        if bRes == False:
            status_code = vdj_response.status_code
            result_final = vdj_response.result
            self.vdj_utils.SaveClientLog(f"HTTP error {status_code}: {result_final}")
            return False
        else:
            return True 
    #------------------------------------------------------------------------------------
    def is_connected(self) -> bool:
        return asyncio.run(self.is_connected_async()) 
    