import sys
import asyncio

from rich.console import Console
console = Console(file=sys.stderr)

from virtualdj_client import VirtualDJClient

#------------------------------------------------------------------------------------------------------------------------------------
def main():
    # Initialize VirtualDJ client
    vdj_client = VirtualDJClient()

    vdj_client_connected = False
    vdj_client_connected = asyncio.run(vdj_client.is_running())
    console.print(f"VirtualDJ connected: {vdj_client_connected}")
    if (vdj_client_connected == False):
        sys.exit()

    vdj_build = asyncio.run(vdj_client.get_build())
    console.print(f"VirtualDJ build: {vdj_build}")

    # vdj_client - test 1
    vdj_script1 = "deck 1 play_pause & loop 4 & crossfader -5%"
    result1 = asyncio.run(vdj_client.executefull(vdj_script1))
    console.print(f"VirtualDJ script < {vdj_script1} > => {result1}")

    # vdj_client - test 2
    result2 = asyncio.run(vdj_client.play('right'))
    console.print(f"VirtualDJ script < deck right play > => {result2}")
#------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
