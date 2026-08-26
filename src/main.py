import sys
from rich.console import Console

from client import VirtualDJClient

#------------------------------------------------------------------------------------------------------------------------------------
def main():
    print("#######################################################")
    print("#  Control VirtualDJ with the Network Control plugin  #")
    print("#######################################################")

    console = Console(file=sys.stderr)

    # Initialize VirtualDJ client
    client = VirtualDJClient()

    client_connected = False
    client_connected = client.run("is_running")
    console.print(f"VirtualDJ connected: {client_connected}")
    if (client_connected == False):
        sys.exit()

    vdj_build = client.run("get_build")
    console.print(f"VirtualDJ script < get_build > => {vdj_build}")

    # test 1a
    result1a = client.run("get_browsed_title_artist")
    console.print(f"VirtualDJ script < get_browsed_title_artist > => {result1a}")

    # test 1b
    result1b = client.run("get_bpm", vdj_deck='left')
    console.print(f"VirtualDJ script < deck left get_bpm > => {result1b}")

    # test 1c
    vdj_script1c = "deck right get_bpm"
    result1c = client.run("query_vdj_script", vdj_script=vdj_script1c)
    console.print(f"VirtualDJ script < {vdj_script1c} > => {result1c}")

    # test 1d
    vdj_script1d = "get_none"
    result1d = client.run("query_vdj_script", vdj_script=vdj_script1d)
    console.print(f"VirtualDJ script < {vdj_script1d} > => {result1d}")

    # test 2a
    vdj_script2a = "deck 1 play_pause & loop 4 & crossfader -5%"
    result2a = client.run("execute_vdj_script", vdj_script=vdj_script2a)
    console.print(f"VirtualDJ script < {vdj_script2a} > => {result2a}")

    # test 2b
    vdj_verb2b = "sync"
    result2b = client.run("execute_vdj_verb", vdj_verb=vdj_verb2b)
    console.print(f"VirtualDJ script < {vdj_verb2b} > => {result2b}")

    # test 2c
    result2c = client.run("play_button", vdj_deck='right')
    console.print(f"VirtualDJ script < deck right play_button > => {result2c}")

    # test 2d
    result2d = client.run("play_pause")
    console.print(f"VirtualDJ script < play_pause > => {result2d}")

    # test 2e
    vdj_verb2e = "loop"
    vdj_params2e = "8"
    result2e = client.run("execute_vdj_verb",vdj_verb=vdj_verb2e, vdj_params=vdj_params2e)
    console.print(f"VirtualDJ script < {vdj_verb2e} {vdj_params2e} > => {result2e}")


#------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
