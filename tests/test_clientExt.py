import pytest
from rich.console import Console

from src.virtualdj_client import VirtualDJClientExt

console = Console()

def test_clientExt():
     # Initialize VirtualDJ client
    client = VirtualDJClientExt()


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

    
    # test 1a
    vdjscript = "get_browsed_title_artist"
    result1a = client.get(vdjscript)
    console.print(f"VirtualDJ script get < {vdjscript} > => {result1a}")

    # test 1b
    vdjscript = "deck left get_bpm"
    result1b = client.get(vdjscript)
    console.print(f"VirtualDJ script get < {vdjscript} > => {result1b}")

    # test 1c
    vdjscript = "deck left get_key"
    result1c = client.get(vdjscript)
    console.print(f"VirtualDJ script get < {vdjscript} > => {result1c}")

    # test 1d
    vdjscript = "get_none"
    result1d = client.get(vdjscript)
    console.print(f"VirtualDJ script get < {vdjscript} > => {result1d}")

    # test 1e
    vdjscript = "deck left get_filepath"
    result1e = client.get(vdjscript)
    console.print(f"VirtualDJ script get < {vdjscript} > => {result1e}")

    # test 1f
    vdjscript = "get_browsed_filepath"
    result1f = client.get(vdjscript)
    console.print(f"VirtualDJ script get < {vdjscript} > => {result1f}")

    # test 1g
    vdjscript = "get_status"
    result1g = client.get(vdjscript)
    console.print(f"VirtualDJ script get < {vdjscript} > => {result1g}")

    # test 1h
    vdjscript = "get_vdj_folder"
    result1h = client.get(vdjscript)
    console.print(f"VirtualDJ script get < {vdjscript} > => {result1h}")

    # test 1i
    vdjscript = "get_browsed_folder_tab"
    result1i = client.get(vdjscript)
    console.print(f"VirtualDJ script get < {vdjscript} > => {result1i}")

    # test 1j
    vdjscript = "get_browsed_folder"
    result1j = client.get(vdjscript)
    console.print(f"VirtualDJ script get < {vdjscript} > => {result1j}")

    # test 1k
    vdjscript = "get_browsed_folder_path"
    result1k = client.get(vdjscript)
    console.print(f"VirtualDJ script get < {vdjscript} > => {result1k}")

    # test 1l
    vdjscript = "get_browsed_folder_scrollsize"
    result1l = client.get(vdjscript)
    console.print(f"VirtualDJ script get < {vdjscript} > => {result1l}")

    # test 1m
    vdjscript = "get_browsed_folder_scrollpos"
    result1m = client.get(vdjscript)
    console.print(f"VirtualDJ script get < {vdjscript} > => {result1m}")
    
    # test 1n
    vdjscript = "get_browsed_scrollsize"
    result1n = client.get(vdjscript)
    console.print(f"VirtualDJ script get < {vdjscript} > => {result1n}")

    # test 1o
    vdjscript = "get_browsed_scrollpos"
    result1o = client.get(vdjscript)
    console.print(f"VirtualDJ script get < {vdjscript} > => {result1o}")

    # test 1p
    vdjscript = "file_count"
    result1p = client.get(vdjscript)
    console.print(f"VirtualDJ script get < {vdjscript} > => {result1p}")

    # test 1q
    vdjscript = "deck left has_stems"
    result1q = client.get(vdjscript)
    console.print(f"VirtualDJ script get < {vdjscript} > => {result1q}")

    # test 1r
    vdjscript = 'setting "loadSecurity"'
    result1r = client.get(vdjscript)
    console.print(f"VirtualDJ script get < {vdjscript} > => {result1r}")

    # test 1s
    vdjscript = 'setting "checkUpdates"'
    result1s = client.get(vdjscript)
    console.print(f"VirtualDJ script get < {vdjscript} > => {result1s}")

    # test 1t
    vdjscript = "get_decks"
    result1t = client.get(vdjscript)
    console.print(f"VirtualDJ script get < {vdjscript} > => {result1t}")
