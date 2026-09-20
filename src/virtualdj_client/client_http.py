""" 
VirtualDJ HTTP API client using the Network Control plugin 
"""
__version__ = '1.0.3'

import httpx
from typing import Literal
from dataclasses import dataclass
from urllib.parse import quote as encodeURI
import logging

from .client_config import VDJ_NETWORK_CONTROL_HOST, VDJ_NETWORK_CONTROL_PORT, VDJ_NETWORK_CONTROL_PASSWORD, VDJ_NETWORK_CONTROL_TIMEOUT

# To limit the number of entries in the log file:
logging.getLogger("httpx").setLevel(logging.WARNING)

#------------------------------------------------------------------------------------
@dataclass
class VdjResponse:
    status: Literal["ok","error"]
    status_code: int
    result: str
#------------------------------------------------------------------------------------------------------------------------------------
class VirtualDJClientHttp:
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
    async def _send_vdj_request(self, vdjscript: str, is_query: bool = False) -> VdjResponse:
        """ Send command via HTTP Network Control plugin """

        headers = {"Content-Type": "text/plain"}
        if VDJ_NETWORK_CONTROL_PASSWORD:
            headers["Authorization"] = f"Bearer {VDJ_NETWORK_CONTROL_PASSWORD}"

        vdj_endpoint = "query" if is_query else "execute"
        vdj_url = f"{self.vdj_base_url}/{vdj_endpoint}"
        encoded_vdjscript = encodeURI(vdjscript)
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
                    return VdjResponse(status=status, status_code=status_code, result=result)
                else:
                    bErr = (result.lower() != "true")
                    status = "error" if bErr else "ok"
                    return VdjResponse(status=status, status_code=status_code, result=result)
            elif status_code == 401:
                status = "error"
                result = "Authentication failed - check password"
                return VdjResponse(status=status, status_code=status_code, result=result)
            else:
                status = "error"
                result = f"{response.text}"
                return VdjResponse(status=status, status_code=status_code, result=result)

        except httpx.ConnectError:
            status = "error"
            status_code = -1
            result = "HTTP Connection error"
            return VdjResponse(status=status, status_code=status_code, result=result)
        except httpx.TimeoutException:
            status = "error"
            status_code = -2
            result = "HTTP timeout"
            return VdjResponse(status=status, status_code=status_code, result=result)
        except httpx.HTTPError as e:
            status = "error"
            status_code = -3
            result = f"{e} It could be a problem of password too."
            return VdjResponse(status=status, status_code=status_code, result=result)
        except Exception as e:
            status = "error"
            status_code = -4
            result = str(e)
            return VdjResponse(status=status, status_code=status_code, result=result)
    #------------------------------------------------------------------------------------
    async def query(self, vdjscript: str) -> VdjResponse:
        """ Query VirtualDJ with a vdjscript """
        vdj_response = await self._send_vdj_request(vdjscript, is_query=True)
        return vdj_response
    #------------------------------------------------------------------------------------    
    async def execute(self, vdjscript: str) -> VdjResponse:
        """ Send command to VirtualDJ with a vdjscript """
        vdj_response = await self._send_vdj_request(vdjscript)
        return vdj_response