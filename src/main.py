import sys
import os
from rich.console import Console
import argparse

from virtualdj_client import VirtualDJClient, VdjDeckData, VdjMixer, VdjDeckEngine, VirtualDJSongsDatabase, VirtualDJHistoryFiles, VirtualDJSettings

console = Console()

#------------------------------------------------------------------------------------------------------------------------------------
def run_VirtualDJ_client():
    print("######################################################")
    print("# Control VirtualDJ with the Network Control plugin  #")
    print("######################################################")

    # Initialize VirtualDJ client
    client = VirtualDJClient()

    # Check if VirtualDJ is running
    client_running = client.is_app_running()
    console.print(f"VirtualDJ running => {client_running}")

    # Launch VirtualDJ if not running
    if client_running == False:
        client_launching = client.open_app()
        console.print(f"VirtualDJ launching => {client_launching}")
        client_running = client.is_app_running()
        console.print(f"VirtualDJ running => {client_running}")
        if (client_running == False):
            sys.exit()

    # Check the NetWork Control plugin
    client_connected = client.is_connected()
    console.print(f"VirtualDJ NetWork Control plugin connected => {client_connected}")
    if (client_connected == False):
        console.print("Check that the NetWork Control plugin is available and activated in VirtualDJ")
        sys.exit()

    console.print("\n")
    mixer: VdjMixer = None
    mixer = client.get_Mixer()
    console.print(f"Mixer = {mixer}")

    console.print("\n")
    decks_count = client.to_int(client.get("get_decks"))
    console.print(f"Total number of decks = {decks_count}")

    console.print("\n")
    leftdeckdata: VdjDeckData = None
    leftdeckdata = client.get_DeckData("left")
    console.print(f"LeftDeck = {leftdeckdata}")

    console.print("\n")
    rightdeckdata: VdjDeckData = None
    rightdeckdata = client.get_DeckData("right")
    console.print(f"RightDeck = {rightdeckdata}")

    if decks_count >= 3:
        console.print("\n")
        deck3data: VdjDeckData = None
        deck3data = client.get_DeckData("3")
        console.print(f"Deck 3 = {deck3data}")

    if decks_count >= 4:
        console.print("\n")
        deck4data: VdjDeckData = None
        deck4data = client.get_DeckData("4")
        console.print(f"Deck 4 = {deck4data}")

    console.print("\n")

#------------------------------------------------------------------------------------------------------------------------------------
def read_VirtualDJ_database():
    print("##############################")
    print("#  Read VirtualDJ database   #")
    print("##############################")

    songsDB = VirtualDJSongsDatabase()
    database_list = songsDB.get_local_database_list()
    console.print(f"VirtualDJ database list => {database_list}")
    for db_path in database_list:
        console.print(f"VirtualDJ database reading => {db_path}")
        database_name = os.path.basename(db_path)
        if (database_name == songsDB.XML_DATABASE_NAME):
            songs_database = songsDB.read_local_xml_database(db_path, filepath_only=False)
            n = len(songs_database)
            if n >= 1:
                song_1 = songs_database[0]
                console.print(f"VirtualDJ database reading => First song of the list = {song_1}")
                song_n = songs_database[n - 1]
                console.print(f"VirtualDJ database reading => Last song of the list = {song_n}")
        elif (database_name == songsDB.SQLITE_CACHE_DB):
            table_name = songsDB.SQLITE_CACHE_DB_WAVEFORMS
            result_list = songsDB.read_local_sqlite_database(db_path,database_name,table_name)
            n = len(result_list)
            if n >= 1:
                item_1 = result_list[0]
                console.print(f"VirtualDJ database reading => First item of {table_name} = {item_1}")
        elif (database_name == songsDB.SQLITE_EXTRA_DB):
            table_name = songsDB.SQLITE_EXTRA_DB_LYRICS
            result_list = songsDB.read_local_sqlite_database(db_path,database_name,table_name)
            n = len(result_list)
            if n >= 1:
                item_1 = result_list[0]
                console.print(f"VirtualDJ database reading => First item of {table_name} = {item_1}")

            table_name = songsDB.SQLITE_EXTRA_DB_RELATED_TRACKS
            result_list = songsDB.read_local_sqlite_database(db_path,database_name,table_name)
            n = len(result_list)
            if n >= 1:
                item_1 = result_list[0]
                console.print(f"VirtualDJ database reading => First item of {table_name} = {item_1}")

            table_name = songsDB.SQLITE_EXTRA_DB_TRACK_DATA
            result_list = songsDB.read_local_sqlite_database(db_path,database_name,table_name)
            n = len(result_list)
            if n >= 1:
                item_1 = result_list[0]
                console.print(f"VirtualDJ database reading => First item of {table_name} = {item_1}")
#------------------------------------------------------------------------------------------------------------------------------------
def read_VirtualDJ_history_files():
    print("#############################")
    print("#  Read VirtualDJ History   #")
    print("#############################")


    history_files = VirtualDJHistoryFiles()
    history_files.get_local_history_files()

#------------------------------------------------------------------------------------------------------------------------------------
def read_VirtualDJ_settings():
    print("#############################")
    print("#  Read VirtualDJ settings  #")
    print("#############################")

    settings = VirtualDJSettings()

    settings_path_list = settings.get_local_settings_path_list()
    console.print(f"VirtualDJ settings path list => {settings_path_list}")
    for settings_path in settings_path_list:
        console.print(f"VirtualDJ settings path reading => {settings_path}")
        result = settings.read_local_xml_settings(settings_path)
        console.print(result)

#------------------------------------------------------------------------------------------------------------------------------------
def client_main_params():
    parser = argparse.ArgumentParser(description="VirtualDJ-API")

    parser.add_argument("-d","--disable", action="store_true", help="Does not load the control of VirtualDJ")
    parser.add_argument("-db", "--database", action="store_true", help="Read the VirtualDJ database")
    parser.add_argument("-ht", "--history", action="store_true", help="Read the VirtualDJ History files")
    parser.add_argument("-st", "--settings", action="store_true", help="Read the VirtualDJ Settings")

    args = parser.parse_args()

    return args
#------------------------------------------------------------------------------------------------------------------------------------
def client_main():
    args = client_main_params()

    if args.database:
        read_VirtualDJ_database()

    if args.history:
        read_VirtualDJ_history_files()

    if args.settings:
        read_VirtualDJ_settings()

    if not args.disable:
        run_VirtualDJ_client()
#------------------------------------------------------------------------------------------------------------------------------------
def main():
    #sys.argv = ["main.py", "--help"]
    #sys.argv = ["main.py", "--disable", "--database"]
    #sys.argv = ["main.py", "--disable", "--history"]
    #sys.argv = ["main.py", "--disable", "--settings"]
    client_main()
#------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
