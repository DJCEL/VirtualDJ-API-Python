import pytest

from src.virtualdj_client import VirtualDJClient


def test_client():
     # Initialize VirtualDJ client
    client = VirtualDJClient()


    vdj_build = client.get("get_build")
    result2a = client.send("deck 1 play_pause & loop 4 & crossfader -5%") 
    result2b = client.send("sync")
    result2c = client.send("deck right play_button")
    result2d = client.send("play_pause")
    result2e = client.send("loop 8")
    result2f = client.send("none")
    result2g = client.send("search 'guetta'")
    result2h = client.send("nothing")
    result2i = client.send("deck right load 'D:\\Music\\xxxx.mp3'")
    result2j = client.send("browser_scroll +1")
    result2k = client.send("save_config")
    result2l = client.send("saveregistryconfig")
    result1a = client.get("get_browsed_title_artist")
    result1b = client.get("deck left get_bpm") 
    result1c = client.get("deck left get_key")
    result1d = client.get("get_none")
    result1e = client.get("deck left get_filepath")
    result1f = client.get("get_browsed_filepath")
    result1g = client.get("get_status")
    result1h = client.get("get_vdj_folder")
    result1i = client.get("get_browsed_folder_tab")
    result1j = client.get("get_browsed_folder")
    result1k = client.get("get_browsed_folder_path")
    result1l = client.get("get_browsed_folder_scrollsize") 
    result1m = client.get("get_browsed_folder_scrollpos")
    result1n = client.get("get_browsed_scrollsize")
    result1o = client.get("get_browsed_scrollpos")
    result1p = client.get("file_count")
    result1q = client.get("deck left has_stems")
    result1r = client.get('setting "loadSecurity"')
    result1s = client.get('setting "checkUpdates"')
    result1t = client.get("get_decks")