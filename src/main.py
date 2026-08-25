import sys
import asyncio
from rich.console import Console

from virtualdj_client import VirtualDJClient

#------------------------------------------------------------------------------------------------------------------------------------
def main():
    print("#######################################################")
    print("#  Control VirtualDJ with the Network Control plugin  #")
    print("#######################################################")

    console = Console(file=sys.stderr)

    # Initialize VirtualDJ client
    vdj_client = VirtualDJClient()

    vdj_client_connected = False
    vdj_client_connected = asyncio.run(vdj_client.is_running())
    console.print(f"VirtualDJ connected: {vdj_client_connected}")
    if (vdj_client_connected == False):
        sys.exit()

    vdj_build = asyncio.run(vdj_client.get_build())
    console.print(f"VirtualDJ script < get_build > => {vdj_build}")

    # vdj_client - test 1a
    result1a = asyncio.run(vdj_client.get_browsed_title_artist())
    console.print(f"VirtualDJ script < get_browsed_title_artist > => {result1a}")

    # vdj_client - test 1b
    result1b = asyncio.run(vdj_client.get_bpm('left'))
    console.print(f"VirtualDJ script < deck left get_bpm > => {result1b}")

    # vdj_client - test 2a
    vdj_script2a = "deck 1 play_pause & loop 4 & crossfader -5%"
    result2a = asyncio.run(vdj_client.executefull(vdj_script2a))
    console.print(f"VirtualDJ script < {vdj_script2a} > => {result2a}")

    # vdj_client - test 2b
    result2b = asyncio.run(vdj_client.play_button('right'))
    console.print(f"VirtualDJ script < deck right play_button > => {result2b}")


#------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
