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

    client_connected = client.run("is_running")
    console.print(f"VirtualDJ connected: {client_connected}")
    if (client_connected == False):
        sys.exit()

    vdj_build = client.get("get_build")
    console.print(f"VirtualDJ script < get_build > => {vdj_build}")

    # test 1a
    result1a = client.get("get_browsed_title_artist")
    console.print(f"VirtualDJ script < get_browsed_title_artist > => {result1a}")

    # test 1b
    result1b = client.get("deck left get_bpm")
    console.print(f"VirtualDJ script < deck left get_bpm > => {result1b}")

    # test 1c
    vdj_script1c = "deck right get_bpm"
    result1c = client.get(vdj_script1c)
    console.print(f"VirtualDJ script < {vdj_script1c} > => {result1c}")

    # test 1d
    vdj_script1d = "get_none"
    result1d = client.get(vdj_script1d)
    console.print(f"VirtualDJ script < {vdj_script1d} > => {result1d}")

    # test 2a
    vdj_script2a = "deck 1 play_pause & loop 4 & crossfader -5%"
    result2a = client.send(vdj_script2a)
    console.print(f"VirtualDJ script < {vdj_script2a} > => {result2a}")

    # test 2b
    vdj_script2b = "sync"
    result2b = client.send(vdj_script2b)
    console.print(f"VirtualDJ script < {vdj_script2b} > => {result2b}")

    # test 2c
    vdj_script2c = "deck right play_button"
    result2c = client.send(vdj_script2c)
    console.print(f"VirtualDJ script < {vdj_script2c} > => {result2c}")

    # test 2d
    result2d = client.send("play_pause")
    console.print(f"VirtualDJ script < play_pause > => {result2d}")

    # test 2e
    vdj_script2e = "loop 8"
    result2e = client.send(vdj_script2e)
    console.print(f"VirtualDJ script < {vdj_script2e} > => {result2e}")

    # test 2f
    vdj_script2f = "none"
    result2f = client.send(vdj_script2f)
    console.print(f"VirtualDJ script < {vdj_script2f} > => {result2f}")


#------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
