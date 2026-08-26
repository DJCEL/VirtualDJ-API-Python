8""" 
VirtualDJ HTTP API client using the Network Control plugin 
"""
__version__ = '1.0.4'

import httpx
import asyncio
from typing import Any, Literal
import psutil
from urllib.parse import quote as encodeURI

from config import VDJ_NETWORK_CONTROL_HOST, VDJ_NETWORK_CONTROL_PORT, VDJ_NETWORK_CONTROL_PASSWORD, VDJ_NETWORK_CONTROL_TIMEOUT
from config import VDJ_PROCESS_NAME


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

        #print(f"vdj_url_full: {vdj_url_full}")

        try:
            async with httpx.AsyncClient(timeout=VDJ_NETWORK_CONTROL_TIMEOUT) as client:
                response = await client.get(vdj_url_full, headers=headers)
                status_code = response.status_code
                if status_code == 200:
                    result = response.text.strip()
                    if is_query:
                        result_len = len(result)
                        bErr = False 
                        if (result_len >= 6):
                            ext_result = result[0:6]
                            bErr = (ext_result.lower() == "error:")
                        status = "error" if bErr else "ok"
                        return {"status": status, "result": result}
                    else:
                        bErr = (result.lower() != "true")
                        status = "error" if bErr else "ok"
                        return {"status": status, "result": result}
                elif status_code == 401:
                    status = "error"
                    result = "Authentication failed - check password"
                    return {"status": status, "result": result}
                else:
                    status = "error"
                    result = f"HTTP {status_code}: {response.text}"
                    return {"status": status, "result": result}
        except httpx.ConnectError:
            status = "error"
            result = "HTTP Connection error"
            return {"status": status, "result": result}
        except httpx.TimeoutException:
            status = "error"
            result = "HTTP timeout"
            return {"status": status, "result": result}
        except httpx.HTTPError as e:
            status = "error"
            result = f"{e} It could be a problem of password too."
            return {"status": status, "result": result}
        except Exception as e:
            status = "error"
            result = str(e)
            return {"status": status, "result": result}
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
    async def querycheck(self, vdj_script: str) -> bool:
        """ Query VirtualDJ with a vdj_script and return status """
        result = await self._query(vdj_script)
        bRes = (result.get("status") == "ok")
        if bRes == False:
            result_final = result.get("result", "Unknown error")
            print(f"{result_final}")
        return bRes
    #------------------------------------------------------------------------------------
    async def query_vdj_script(self, vdj_script: str) -> dict[str, Any]:
        """ Query VirtualDJ with a vdj_script """
        result = await self._query(vdj_script)
        bRes = (result.get("status") == "ok")
        if (bRes == True):
            result_final = result.get("result", "")
            return result_final
        else:
            result_final = result.get("result", "Unknown error")
            #raise VDJError(f"Failed to query < {vdj_script} >: {result_final}")
            return f"Failed to query < {vdj_script} >: {result_final}"
            
    #------------------------------------------------------------------------------------
    async def execute_vdj_script(self, vdj_script: str) -> bool:
        """ Execute a vdj_script and return status """
        result = await self._execute(vdj_script)
        bRes = (result.get("status") == "ok")
        if (bRes == True):
            bRes2 = (result.get("result", "").lower() == "true")
            return bRes2
        else:
            return False
    #------------------------------------------------------------------------------------
    def run(self, async_fn_name: str, *args, **kwargs):
        async_fn = getattr(self, async_fn_name)
        return asyncio.run(async_fn(*args, **kwargs))
    #------------------------------------------------------------------------------------
    def send(self, vdj_script: str):
        return asyncio.run(execute_vdj_script(vdj_script))
    #------------------------------------------------------------------------------------
    def get(self, vdj_script: str):
        return asyncio.run(query_vdj_script(vdj_script))
    #------------------------------------------------------------------------------------
    #  VirtualDJ queries - specific
     #------------------------------------------------------------------------------------
    async def is_running(self) -> bool:
        """ Check if VirtualDJ software is running and Network Control Plugin is responding """
        vdj_script = "get_version"

        for proc in psutil.process_iter(["pid", "name"]):
            process_name = proc.info["name"].lower()
            if process_name and VDJ_PROCESS_NAME in process_name:
                result = await self.querycheck(vdj_script)
                return result

        return False

     #------------------------------------------------------------------------------------
    async def get_variable(self, vdj_variable: str) -> Any:
        """ Get a value of a VirtualDJ variable """
        vdj_script = f"get_var '{vdj_variable}'"
        result = await self.query_vdj_script(vdj_script)
        return result
     
     #------------------------------------------------------------------------------------
    # VirtualDJ tools
    #------------------------------------------------------------------------------------
    def vdjscript_and(vdj_script1:str, vdj_script2:str):
        vdj_script_full = vdj_script1 + ' & ' + vdj_script2
        return vdj_script_full
    #------------------------------------------------------------------------------------
    def vdjscript_if_then_else(vdj_script_condition:str, vdj_script_if_true:str, vdj_script_if_false:str):
        vdj_script_full = vdj_script_condition + ' ? ' + vdj_script_if_true + " : " + vdj_script_if_false
        return vdj_script_full