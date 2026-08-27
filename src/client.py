""" 
VirtualDJ HTTP API client using the Network Control plugin 
"""
__version__ = '1.0.8'

import httpx
import asyncio
from typing import Any, Literal
import psutil
from urllib.parse import quote as encodeURI
import logging

from config import VDJ_NETWORK_CONTROL_HOST, VDJ_NETWORK_CONTROL_PORT, VDJ_NETWORK_CONTROL_PASSWORD, VDJ_NETWORK_CONTROL_TIMEOUT, VDJ_NETWORK_CONTROL_DEBUG
from config import VDJ_PROCESS_NAME

logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------------------------------------------------------------
def CreateClientLog():
    LOG_FOLDER = './log'
    LOG_FILENAME = 'client.log'

    if VDJ_NETWORK_CONTROL_DEBUG:
        import os
        if not os.path.exists(LOG_FOLDER):
            os.makedirs(LOG_FOLDER)
        logging.basicConfig(filename=f"{LOG_FOLDER}/{LOG_FILENAME}", level=logging.INFO)
#------------------------------------------------------------------------------------------------------------------------------------
def SaveClientLog(msg):
    if VDJ_NETWORK_CONTROL_DEBUG:
        logger.info(msg)
#------------------------------------------------------------------------------------------------------------------------------------
class VDJDeck:
    name : Literal['left', 'right', 'leftvideo', 'rightvideo', 'all', 'default', 'active', 'master']
    id : int
#------------------------------------------------------------------------------------------------------------------------------------
class VDJError(Exception):
    """VirtualDJ operation error"""
    pass
#------------------------------------------------------------------------------------------------------------------------------------
class VirtualDJClient:
    def __init__(self):
        self.vdj_base_url = f"http://{VDJ_NETWORK_CONTROL_HOST}:{VDJ_NETWORK_CONTROL_PORT}"
        self._client: httpx.AsyncClient | None = None
        CreateClientLog()
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
    async def _send_vdj_request(self, vdj_script: str, is_query: bool = False) -> dict[str, Any]:
        """ Send command via HTTP Network Control plugin """
        vdj_endpoint = "query" if is_query else "execute"
        headers = self._get_headers()
        vdj_url = f"{self.vdj_base_url}/{vdj_endpoint}"
        encoded_vdjscript = encodeURI(vdj_script)
        vdj_url_full = f"{vdj_url}?script={encoded_vdjscript}"

        try:
            #aync with self._client as http_client:
            async with httpx.AsyncClient(timeout=VDJ_NETWORK_CONTROL_TIMEOUT) as http_client:
                response = await http_client.get(vdj_url_full, headers=headers)
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
                        return {"status": status, "status_code": {status_code}, "result": result}
                    else:
                        bErr = (result.lower() != "true")
                        status = "error" if bErr else "ok"
                        return {"status": status, "status_code": {status_code},"result": result}
                elif status_code == 401:
                    status = "error"
                    result = "Authentication failed - check password"
                    return {"status": status, "status_code": {status_code}, "result": result}
                else:
                    status = "error"
                    result = f"{response.text}"
                    return {"status": status, "status_code": {status_code}, "result": result}
        except httpx.ConnectError:
            status = "error"
            status_code = -1
            result = "HTTP Connection error"
            return {"status": status,"status_code": {status_code}, "result": result}
        except httpx.TimeoutException:
            status = "error"
            status_code = -2
            result = "HTTP timeout"
            return {"status": status, "status_code": {status_code}, "result": result}
        except httpx.HTTPError as e:
            status = "error"
            status_code = -3
            result = f"{e} It could be a problem of password too."
            return {"status": status, "status_code": {status_code}, "result": result}
        except Exception as e:
            status = "error"
            status_code = -4
            result = str(e)
            return {"status": status, "status_code": {status_code}, "result": result}
    #------------------------------------------------------------------------------------
    async def _query(self, vdj_script: str) -> dict[str, Any]:
        """ Query VirtualDJ with a vdj_script """
        result = await self._send_vdj_request(vdj_script, is_query=True)
        return result
    #------------------------------------------------------------------------------------       
    async def _execute(self, vdj_script: str) -> dict[str, Any]:
        """ Send command to VirtualDJ with a vdj_script """
        result = await self._send_vdj_request(vdj_script)
        return result
    #------------------------------------------------------------------------------------
    async def _query_vdj_script(self, vdj_script: str) -> str:
        """ Query VirtualDJ with a vdj_script """
        result = await self._query(vdj_script)
        bRes = (result.get("status") == "ok")
        if (bRes == True):
            result_final = result.get("result", "")
            return result_final
        else:
            status_code = result.get("status_code")
            result_final = result.get("result", "Unknown error")
            SaveClientLog(f"HTTP error {status_code}: {result_final}")
            return f"Failed to query < {vdj_script} >: {result_final}"
            
    #------------------------------------------------------------------------------------
    async def _execute_vdj_script(self, vdj_script: str) -> bool:
        """ Execute a vdj_script and return status """
        result = await self._execute(vdj_script)
        bRes = (result.get("status") == "ok")
        if (bRes == True):
            bRes2 = (result.get("result", "").lower() == "true")
            return bRes2
        else:
            status_code = result.get("status_code")
            result_final = result.get("result", "Unknown error")
            SaveClientLog(f"HTTP error {status_code}: {result_final}")
            return False
    
    #------------------------------------------------------------------------------------
    def send(self, vdj_script: str) -> bool:
        return asyncio.run(self._execute_vdj_script(vdj_script))
    #------------------------------------------------------------------------------------
    def get(self, vdj_script: str) -> str:
        return asyncio.run(self._query_vdj_script(vdj_script))
    #------------------------------------------------------------------------------------
    #  Check if VirtualDJ is connected
    #------------------------------------------------------------------------------------
    async def _query_vdj_script_test(self, vdj_script: str) -> bool:
        """ Test VirtualDJ with a vdj_script and return status """
        result = await self._query(vdj_script)
        bRes = (result.get("status") == "ok")
        if bRes == False:
            status_code = result.get("status_code")
            result_final = result.get("result", "Unknown error")
            SaveClientLog(f"HTTP error {status_code}: {result_final}")
        return bRes
    #------------------------------------------------------------------------------------
    async def _is_virtualdj_connected(self) -> bool:
        """ Check if VirtualDJ software is running and Network Control Plugin is responding """
        for proc in psutil.process_iter(["pid", "name"]):
            process_name = proc.info["name"].lower()
            if process_name and VDJ_PROCESS_NAME in process_name:
                result = await self._query_vdj_script_test("get_version")
                return result

        return False
    #------------------------------------------------------------------------------------
    def is_connected(self) -> bool:
        return asyncio.run(self._is_virtualdj_connected()) 
    #------------------------------------------------------------------------------------
    # VirtualDJ tools
    #------------------------------------------------------------------------------------
    def vdjscript_and(vdj_script1:str, vdj_script2:str) -> str:
        vdj_script_full = vdj_script1 + ' & ' + vdj_script2
        return vdj_script_full
    #------------------------------------------------------------------------------------
    def vdjscript_if_then_else(vdj_script_condition:str, vdj_script_if_true:str, vdj_script_if_false:str) -> str:
        vdj_script_full = vdj_script_condition + ' ? ' + vdj_script_if_true + " : " + vdj_script_if_false
        return vdj_script_full