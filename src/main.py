import sys
import asyncio
from rich.console import Console

from virtualdj_client import VirtualDJClient

#------------------------------------------------------------------------------------------------------------------------------------
def main():
    print("##############################################################")
    print("# Control VirtualDJ with the Network Control plugin #")
    print("##############################################################")

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

    # vdj_client - test 1
    result1 = asyncio.run(vdj_client.get_browsed_title_artist())
    console.print(f"VirtualDJ script < get_browsed_title_artist > => {result1}")

    # vdj_client - test 2
    vdj_script2 = "deck 1 play_pause & loop 4 & crossfader -5%"
    result2 = asyncio.run(vdj_client.executefull(vdj_script2))
    console.print(f"VirtualDJ script < {vdj_script2} > => {result2}")

    # vdj_client - test 3
    result3 = asyncio.run(vdj_client.play_button('right'))
    console.print(f"VirtualDJ script < deck right play_button > => {result3}")


#------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
