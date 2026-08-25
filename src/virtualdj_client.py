""" 
VirtualDJ HTTP API client using the Network Control plugin 
"""
import httpx
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

        # print(f"vdj_url_full: {vdj_url_full}")

        try:
            async with httpx.AsyncClient(timeout=VDJ_NETWORK_CONTROL_TIMEOUT) as client:
                response = await client.get(vdj_url_full, headers=headers)
                if response.status_code == 200:
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
                elif response.status_code == 401:
                    status = "error"
                    result = "Authentication failed - check password"
                    return {"status": status, "result": result}
                else:
                    status = "error"
                    result = f"HTTP {response.status_code}: {response.text}"
                    return {"status": status, "result": result}
        except httpx.ConnectError:
            status = "error"
            result = "HTTP Connection error"
            return {"status": status, "result": result}
        except httpx.TimeoutException:
            status = "error"
            result = "HTTP timeout"
            return {"status": status, "result": result}
        except Exception as e:
            status = "error"
            result = str(e)
            return {"status": status, "result": result}
    #------------------------------------------------------------------------------------
    async def query(self, vdj_script: str) -> dict[str, Any]:
        """ Query VirtualDJ with a vdj_script """
        result = await self._send_vdj_request(vdj_script, is_query=True)
        return result
    #------------------------------------------------------------------------------------       
    async def execute(self, vdj_script: str) -> dict[str, Any]:
        """ Send command to VirtualDJ with a vdj_script """
        result = await self._send_vdj_request(vdj_script)
        return result
    #------------------------------------------------------------------------------------
    async def querycheck(self, vdj_script: str) -> bool:
        """ Query VirtualDJ with a vdj_script and return status """
        result = await self.query(vdj_script)
        bRes = (result.get("status") == "ok")
        return bRes
    #------------------------------------------------------------------------------------
    async def queryfull(self, vdj_script: str) -> dict[str, Any]:
        """ Query VirtualDJ with a vdj_script """
        result = await self.query(vdj_script)
        bRes = (result.get("status") == "ok")
        if (bRes == True):
            result_final = result.get("result", "")
            return result_final
        else:
            raise VDJError(f"Failed to query {vdj_script}: {result.get("result", "Unknown error")}")
    #------------------------------------------------------------------------------------
    async def executefull(self, vdj_script: str) -> bool:
        """ Execute a vdj_script and return status """
        result = await self.execute(vdj_script)
        bRes = (result.get("status") == "ok")
        if (bRes == True):
            bRes2 = (result.get("result", "").lower() == "true")
            return bRes2
        else:
            return False
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
    async def get_build(self) -> Any:
        """ Get the VirtualDJ build """
        vdj_script = "get_build"
        result = await self.queryfull(vdj_script)
        return result
    #------------------------------------------------------------------------------------
    async def get_variable(self, vdj_variable: str) -> Any:
        """ Get a value of a VirtualDJ variable """
        vdj_script = f"get_var '{vdj_variable}'"
        result = await self.queryfull(vdj_script)
        return result


    #------------------------------------------------------------------------------------
    # VirtualDJ executes - specific
    #------------------------------------------------------------------------------------
    async def executefull_verb_deck(self, vdj_verb: str, vdj_deck: str = None) -> bool:
        """ Execute a vdj_script on a deck and return status """
        if vdj_deck is None:
            vdj_script = f"{vdj_verb}"
        else:
            vdj_script = f"deck {vdj_deck} {vdj_verb}"
        result = await self.executefull(vdj_script)
        return result
    #------------------------------------------------------------------------------------
    async def play(self, vdj_deck: str) -> bool:
        """ Play a deck"""
        vdj_script = f"deck {vdj_deck} play"
        result = await self.executefull(vdj_script)
        return result
    #------------------------------------------------------------------------------------
    async def pause(self, vdj_deck: str) -> bool:
        """ Pause a deck """
        vdj_script = f"deck {vdj_deck} pause"
        result = await self.executefull(vdj_script)
        return result
    #------------------------------------------------------------------------------------
    async def stop(self, vdj_deck: str) -> bool:
        """ Stop a deck """
        vdj_script = f"deck {vdj_deck} stop"
        result = await self.executefull(vdj_script)
        return result
    #------------------------------------------------------------------------------------ 
    async def play_pause(self, vdj_deck: str) -> bool:
        """ Toggle between play and pause on a deck """
        vdj_script = f"deck {vdj_deck} play_pause"
        result = await self.executefull(vdj_script)
        return result
    #------------------------------------------------------------------------------------
    async def play_button(self, vdj_deck: str) -> bool:
        """ play_button a deck """
        vdj_script = f"deck {vdj_deck} play_button"
        result = await self.executefull(vdj_script)
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