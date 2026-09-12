import sys
import os
from rich.console import Console
import argparse

from virtualdj_client import VirtualDJClient, VirtualDJClientExt, VdjDeckData, VirtualDJSongsDatabase, VirtualDJHistoryFiles, VirtualDJSettings

console = Console()

#------------------------------------------------------------------------------------------------------------------------------------
def control_VirtualDJ():
    print("#######################################################")
    print("#  Control VirtualDJ with the Network Control plugin  #")
    print("#######################################################")

    # Initialize VirtualDJ client
    client = VirtualDJClient()

    
    # Check if VirtualDJ is running
    client_running = client.is_app_running()
    console.print(f"VirtualDJ running => {client_running}")

    # Launch VirtualDJ if not running
    if client_running == False:
        console.print("Launching VirtualDJ...")
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

    vdj_script = "get_build"
    vdj_build = client.get(vdj_script)
    console.print(f"VirtualDJ script get < {vdj_script} > => {vdj_build}")

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

    # test 2g
    vdj_script = "search 'guetta'"
    result2g = client.send(vdj_script)
    console.print(f"VirtualDJ script send < {vdj_script} > => {result2g}")

    # test 2h
    vdj_script = "nothing"
    result2h = client.send(vdj_script)
    console.print(f"VirtualDJ script send < {vdj_script} > => {result2h}")

    # test 2i (update with your own filepath)
    filepath = "D:\\Music\\xxxx.mp3"
    vdj_script = f"deck right load '{filepath}'"
    result2i = client.send(vdj_script)
    console.print(f"VirtualDJ script send < {vdj_script} > => {result2i}")

    # test 2j
    vdj_script = "browser_scroll +1"
    result2j = client.send(vdj_script)
    console.print(f"VirtualDJ script send < {vdj_script} > => {result2j}")

    # test 2k
    vdj_script = "save_config"
    result2k = client.send(vdj_script)
    console.print(f"VirtualDJ script send < {vdj_script} > => {result2k}")

    # test 2l
    vdj_script = "saveregistryconfig"
    result2l = client.send(vdj_script)
    console.print(f"VirtualDJ script send < {vdj_script} > => {result2l}")
    
    # test 1a
    vdj_script = "get_browsed_title_artist"
    result1a = client.get(vdj_script)
    console.print(f"VirtualDJ script get < {vdj_script} > => {result1a}")

    # test 1b
    vdj_script = "deck left get_bpm"
    result1b = client.get(vdj_script)
    console.print(f"VirtualDJ script get < {vdj_script} > => {result1b}")

    # test 1c
    vdj_script = "deck left get_key"
    result1c = client.get(vdj_script)
    console.print(f"VirtualDJ script get < {vdj_script} > => {result1c}")

    # test 1d
    vdj_script = "get_none"
    result1d = client.get(vdj_script)
    console.print(f"VirtualDJ script get < {vdj_script} > => {result1d}")

    # test 1e
    vdj_script = "deck left get_filepath"
    result1e = client.get(vdj_script)
    console.print(f"VirtualDJ script get < {vdj_script} > => {result1e}")

    # test 1f
    vdj_script = "get_browsed_filepath"
    result1f = client.get(vdj_script)
    console.print(f"VirtualDJ script get < {vdj_script} > => {result1f}")

    # test 1g
    vdj_script = "get_status"
    result1g = client.get(vdj_script)
    console.print(f"VirtualDJ script get < {vdj_script} > => {result1g}")

    # test 1h
    vdj_script = "get_vdj_folder"
    result1h = client.get(vdj_script)
    console.print(f"VirtualDJ script get < {vdj_script} > => {result1h}")

    # test 1i
    vdj_script = "get_browsed_folder_tab"
    result1i = client.get(vdj_script)
    console.print(f"VirtualDJ script get < {vdj_script} > => {result1i}")

    # test 1j
    vdj_script = "get_browsed_folder"
    result1j = client.get(vdj_script)
    console.print(f"VirtualDJ script get < {vdj_script} > => {result1j}")

    # test 1k
    vdj_script = "get_browsed_folder_path"
    result1k = client.get(vdj_script)
    console.print(f"VirtualDJ script get < {vdj_script} > => {result1k}")

    # test 1l
    vdj_script = "get_browsed_folder_scrollsize"
    result1l = client.get(vdj_script)
    console.print(f"VirtualDJ script get < {vdj_script} > => {result1l}")

    # test 1m
    vdj_script = "get_browsed_folder_scrollpos"
    result1m = client.get(vdj_script)
    console.print(f"VirtualDJ script get < {vdj_script} > => {result1m}")
    
    # test 1n
    vdj_script = "get_browsed_scrollsize"
    result1n = client.get(vdj_script)
    console.print(f"VirtualDJ script get < {vdj_script} > => {result1n}")

    # test 1o
    vdj_script = "get_browsed_scrollpos"
    result1o = client.get(vdj_script)
    console.print(f"VirtualDJ script get < {vdj_script} > => {result1o}")

    # test 1p
    vdj_script = "file_count"
    result1p = client.get(vdj_script)
    console.print(f"VirtualDJ script get < {vdj_script} > => {result1p}")

    # test 1q
    vdj_script = "deck left has_stems"
    result1q = client.get(vdj_script)
    console.print(f"VirtualDJ script get < {vdj_script} > => {result1q}")

    # test 1r
    vdj_script = 'setting "loadSecurity"'
    result1r = client.get(vdj_script)
    console.print(f"VirtualDJ script get < {vdj_script} > => {result1r}")

    # test 1s
    vdj_script = 'setting "checkUpdates"'
    result1s = client.get(vdj_script)
    console.print(f"VirtualDJ script get < {vdj_script} > => {result1s}")

    # test 1t
    vdj_script = "get_decks"
    result1t = client.get(vdj_script)
    console.print(f"VirtualDJ script get < {vdj_script} > => {result1t}")


    # Close VirtualDJ
    #console.print(f"VirtualDJ closing...")
    #client.close_app()

#------------------------------------------------------------------------------------------------------------------------------------
def run_VirtualDJ_clientExt():
    print("################################################################")
    print("# Control VirtualDJ with the Network Control plugin (Extended) #")
    print("################################################################")

    # Initialize VirtualDJ clientExt
    client = VirtualDJClientExt()

    # Check if VirtualDJ is running
    client_running = client.is_app_running()
    console.print(f"VirtualDJ running => {client_running}")

    # Launch VirtualDJ if not running
    if client_running == False:
        console.print("Launching VirtualDJ...")
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


    deckdata: VdjDeckData = None
    deckdata = client.get_DeckData("left")

    console.print("Left deck:")
    console.print(deckdata)

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
    parser.add_argument("-ext", "--extended", action="store_true", help="Use the VirtualDJ clientExt version")

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

    if args.extended:
        run_VirtualDJ_clientExt()

    if not args.disable:
        control_VirtualDJ()
#------------------------------------------------------------------------------------------------------------------------------------
def main():
    #sys.argv = ["main.py", "--help"]
    #sys.argv = ["main.py", "--disable", "--database"]
    #sys.argv = ["main.py", "--disable", "--history"]
    #sys.argv = ["main.py", "--disable", "--settings"]
    sys.argv = ["main.py", "--disable", "--extended"]
    client_main()
#------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
