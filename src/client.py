""" 
VirtualDJ HTTP API client using the Network Control plugin 
"""
__version__ = '1.0.14'

import httpx
import asyncio
from typing import Any, Literal, TypedDict
import psutil
from urllib.parse import quote as encodeURI
import logging
import os
import subprocess
import platform
import xml.etree.ElementTree as ET

from config import VDJ_NETWORK_CONTROL_HOST, VDJ_NETWORK_CONTROL_PORT, VDJ_NETWORK_CONTROL_PASSWORD, VDJ_NETWORK_CONTROL_TIMEOUT, VDJ_NETWORK_CONTROL_DEBUG
from config import VDJ_PROCESS_NAME, VDJ_PROCESS_PATH_WINDOWS, VDJ_PROCESS_PATH_MAC

logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------------------------------------------------------------
def _CreateClientLog():
    LOG_FOLDER = './log'
    LOG_FILENAME = 'client.log'

    filepath = f"{LOG_FOLDER}/{LOG_FILENAME}"

    if VDJ_NETWORK_CONTROL_DEBUG:
        if not os.path.exists(LOG_FOLDER):
            os.makedirs(LOG_FOLDER)
        logging.basicConfig(filename=filepath, level=logging.INFO)
#------------------------------------------------------------------------------------------------------------------------------------
def _SaveClientLog(msg):
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
        _CreateClientLog()
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
            _SaveClientLog(f"HTTP error {status_code}: {result_final}")
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
            _SaveClientLog(f"HTTP error {status_code}: {result_final}")
            return False
    #------------------------------------------------------------------------------------
    def send(self, vdj_script: str) -> bool:
        return asyncio.run(self._execute_vdj_script(vdj_script))
    #------------------------------------------------------------------------------------
    def get(self, vdj_script: str) -> str:
        return asyncio.run(self._query_vdj_script(vdj_script))
    #------------------------------------------------------------------------------------
    #  Launch / Quit VirtualDJ
    #------------------------------------------------------------------------------------
    def is_app_running(self) -> bool:
        """ Check if VirtualDJ software is running """
        bRes = False
        for proc in psutil.process_iter(["pid", "name"]):
            process_name = proc.info["name"].lower()
            if process_name and VDJ_PROCESS_NAME in process_name:
                bRes = True

        return bRes
    #------------------------------------------------------------------------------------
    def open_app(self) -> bool:
        """ Open VirtuaDJ """
        is_vdj_running = self.is_app_running()
        if is_vdj_running == True:
            return True

        system = platform.system()
        if system == "Windows":
            app_path = VDJ_PROCESS_PATH_WINDOWS
        elif system == "Darwin":
            app_path = os.path.join(VDJ_PROCESS_PATH_MAC,"Contents","MacOS","VirtualDJ")
        else:
            return False

        if not os.path.exists(app_path):
            raise FileNotFoundError(f"VirtualDJ not found: {app_path}")
            _SaveClientLog(f"VirtualDJ not found: {app_path}")
            return False

        # TODO: check if updates are activated in VirtualDJ via settings.xml

        # Open the application in background:
        try:
            subprocess.Popen([app_path], 
                             stdin=subprocess.DEVNULL, 
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL,
                             creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS,
                             start_new_session=True)
        except Exception as e:
            msg =  app_path + "\n" + str(e)
            print(msg)
            _SaveClientLog(msg)
            return False

        return True
    #------------------------------------------------------------------------------------
    def close_app(self, force_close: bool = False) -> bool:
        """ Close VirtuaDJ """
        is_vdj_running = self.is_app_running()
        if is_vdj_running == False:
            return True

        is_vdj_connected = self.is_connected()
        if is_vdj_connected == True:
            # TODO: Bypass the VirtualDJ security at exit if (force_close == True)
            vdj_script = "close"
            result = self.send(vdj_script)
            if result == True:
                return True

        # TODO: Force kill app if (force_close == True)
        return False
    #------------------------------------------------------------------------------------
    #  Check if VirtualDJ is connected
    #------------------------------------------------------------------------------------
    async def _is_virtualdj_connected(self) -> bool:
        """ Check if VirtualDJ software is running and Network Control Plugin is responding """
        is_vdj_running = self.is_app_running()
        if is_vdj_running == False:
            return False

        vdj_script = "get_version"
        result = await self._query(vdj_script)
        bRes = (result.get("status") == "ok")
        if bRes == False:
            status_code = result.get("status_code")
            result_final = result.get("result", "Unknown error")
            _SaveClientLog(f"HTTP error {status_code}: {result_final}")
            return False
        else:
            return True
    #------------------------------------------------------------------------------------
    def is_connected(self) -> bool:
        return asyncio.run(self._is_virtualdj_connected()) 
    #------------------------------------------------------------------------------------
    # VirtualDJ script tools
    #------------------------------------------------------------------------------------
    def vdjscript_and(vdj_script1:str, vdj_script2:str) -> str:
        vdj_script_full = vdj_script1 + ' & ' + vdj_script2
        return vdj_script_full
    #------------------------------------------------------------------------------------
    def vdjscript_if_then_else(vdj_script_condition:str, vdj_script_if_true:str, vdj_script_if_false:str) -> str:
        vdj_script_full = vdj_script_condition + ' ? ' + vdj_script_if_true + " : " + vdj_script_if_false
        return vdj_script_full
    #------------------------------------------------------------------------------------
    # VirtualDJ databases
    #------------------------------------------------------------------------------------
    class VDJPoiType:
        name : Literal['automix','beatgrid','remix']
    #------------------------------------------------------------------------------------
    class VDJPoiPoint:
        name : Literal['realStart','realEnd','fadeStart','fadeEnd','cutStart','cutEnd','tempoStart','tempoEnd']
    #------------------------------------------------------------------------------------
    class VdjPoi(TypedDict):
        Name: str
        Pos: float
        Type: str
        Point: str
   #------------------------------------------------------------------------------------
    class VdjSong():
       FilePath: str
       FileSize: int
       Flag: int
       Tags_Author: str
       Tags_Title: str
       Tags_Year: int
       Tags_Genre: str
       Tags_Bpm: int
       Tags_Key: int
       Tags_Album: str
       Tags_Composer: str
       Tags_Label: str
       Tags_TrackNumber: str
       Tags_Remix: str
       Tags_Stars: int
       Tags_Remixer: str
       Tags_Grouping: str
       Tags_User1: str
       Tags_User2: str
       Tags_Internal: str
       Tags_Flag: int
       Infos_SongLength: float
       Infos_LastModified: int
       Infos_FirstSeen: int
       Infos_FirstPlay: int
       Infos_LastPlay: int
       Infos_PlayCount: int
       Infos_Bitrate: int
       Infos_Cover: int
       Infos_Color: str
       Infos_Corrupted: int
       Infos_Gain: int
       Infos_UserColor: str
       Comment: str
       Scan_Version: int
       Scan_Bpm: float
       Scan_Phase: float
       Scan_AltBpm: float
       Scan_Rigid: float
       Scan_Volume: float
       Scan_Key: str
       Scan_AudioSig: str
       Scan_Flag: int
       Scan_Beatgrid: list[str]
       Poi: list[VdjPoi]
       Link_NetSearch: str
       Link_Cover: str
    #------------------------------------------------------------------------------------
    def get_local_database_list(self):
        database_list = []
        xml_database_name = "database.xml"
        system = platform.system()

        client_connected = self.is_connected()
        if client_connected == True:
            main_virtualdj_path = self.get("get_vdj_folder")
            main_XMLdatabase_path = os.path.join(main_virtualdj_path, xml_database_name)
            if os.path.exists(main_XMLdatabase_path):
                database_list.append(main_XMLdatabase_path)

        if system == "Windows":
            appData_Local = os.getenv('LOCALAPPDATA')
            main_XMLdatabase_path = os.path.join(appData_Local, 'VirtualDJ', xml_database_name)
            if os.path.exists(main_XMLdatabase_path):
                database_list.append(main_XMLdatabase_path)

            drives_Windows = [ chr(x) + ":" for x in range(65,91) if os.path.exists(chr(x) + ":") ]

            for drive in drives_Windows:
                drive_full = drive + "\\"
                external_XMLdatabase_path = os.path.join(drive_full,'VirtualDJ', xml_database_name)
                if os.path.exists(external_XMLdatabase_path):
                    database_list.append(external_XMLdatabase_path)

            database_list_noduplicates = list(dict.fromkeys(database_list))

            return database_list_noduplicates

        elif system == "Darwin":
            #TODO: list of drives
            return database_list

        return database_list
    #------------------------------------------------------------------------------------
    def read_local_XMLdatabase(self, database_path: str, readAllSongs: bool = False):
        tree = ET.parse(database_path)
        root = tree.getroot()
        root_tag = root.tag
        id = 0
        songs_count = 0

        xmlTag_Song = ["Song"]
        xmlTag_Song_Data = ["Tags","Infos","Scan","CustomMix","Link"]
        xmlTag_Song_Poi = ["Poi"]
        xmlTag_Song_Comment = ["Comment"]


        if root_tag == "VirtualDJ_Database":
            root_attrib = root.attrib
            print(f"VirtualDJ database reading => {root_attrib}")
            songs_count = len(root.findall(".//" +  xmlTag_Song[0]))
            print(f"VirtualDJ database reading => Number of songs found = {songs_count}")
            if readAllSongs:
                for child in root:
                    child_tag = child.tag
                    if child_tag in xmlTag_Song:
                        i = 0
                        id = id + 1
                        child_attrib = child.attrib
                        child_text = child.text
                        print(child_tag + str(id)+ ": " + str(child_attrib))
                        for subchild in child:
                            subchild_tag = subchild.tag
                            if subchild_tag in xmlTag_Song_Data:
                               subchild_attrib = subchild.attrib
                               subchild_text = subchild.text
                               print(child_tag + str(id) + "_" + subchild_tag + ": " + str(subchild_attrib))
                            elif subchild_tag in xmlTag_Song_Poi:
                               i = i + 1
                               subchild_attrib = subchild.attrib
                               subchild_text = subchild.text
                               print(child_tag + str(id) + "_" + subchild_tag + str(i) + ": " + str(subchild_attrib))
                            elif subchild_tag in xmlTag_Song_Comment:
                                subchild_attrib = subchild.attrib
                                subchild_text = subchild.text
                                print(child_tag + str(id) + "_" + subchild_tag + ": " + str(subchild_text))
                            else:
                                print(f"subchild_tag < {subchild_tag} > not defined")
