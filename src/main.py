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

    client_connected = client.is_connected()
    console.print(f"VirtualDJ connected: {client_connected}")
    if (client_connected == False):
        sys.exit()

    vdj_script = "get_build"
    vdj_build = client.get(vdj_script)
    console.print(f"VirtualDJ script get < {vdj_script} > => {vdj_build}")

    # test 1a
    vdj_script = "get_browsed_title_artist"
    result1a = client.get(vdj_script)
    console.print(f"VirtualDJ script get < {vdj_script} > => {result1a}")

    # test 1b
    vdj_script = "deck left get_bpm"
    result1b = client.get(vdj_script)
    console.print(f"VirtualDJ script get < {vdj_script} > => {result1b}")

    # test 1c
    vdj_script = "deck right get_key"
    result1c = client.get(vdj_script)
    console.print(f"VirtualDJ script get < {vdj_script} > => {result1c}")

    # test 1d
    vdj_script = "get_none"
    result1d = client.get(vdj_script)
    console.print(f"VirtualDJ script get < {vdj_script} > => {result1d}")

    # test 2a
    vdj_script = "deck 1 play_pause & loop 4 & crossfader -5%"
    result2a = client.send(vdj_script)
    console.print(f"VirtualDJ script send < {vdj_script} > => {result2a}")

    # test 2b
    vdj_script = "sync"
    result2b = client.send(vdj_script)
    console.print(f"VirtualDJ script send < {vdj_script} > => {result2b}")

    # test 2c
    vdj_script = "deck right play_button"
    result2c = client.send(vdj_script)
    console.print(f"VirtualDJ script send < {vdj_script} > => {result2c}")

    # test 2d
    vdj_script = "play_pause"
    result2d = client.send(vdj_script)
    console.print(f"VirtualDJ script send < {vdj_script} > => {result2d}")

    # test 2e
    vdj_script = "loop 8"
    result2e = client.send(vdj_script)
    console.print(f"VirtualDJ script send < {vdj_script} > => {result2e}")

    # test 2f
    vdj_script = "none"
    result2f = client.send(vdj_script)
    console.print(f"VirtualDJ script send < {vdj_script} > => {result2f}")


#------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
