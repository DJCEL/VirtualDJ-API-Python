# Client - Debug
VDJ_CLIENT_DEBUG = True # default (bool): True


# VirtualDJ - Network Control Plugin (HTTP Server)
VDJ_NETWORK_CONTROL_HOST = "127.0.0.1" # default (str): "127.0.0.1"
VDJ_NETWORK_CONTROL_PORT = 80 # default (int): 80
VDJ_NETWORK_CONTROL_PASSWORD = None # default (str): None
VDJ_NETWORK_CONTROL_TIMEOUT = 10.0  # default (int): 10 seconds

# VirtualDJ - Process name in tasks manager
VDJ_PROCESS_NAME = "virtualdj"
VDJ_PROCESS_PATH_WINDOWS = r"C:\Program Files\VirtualDJ\virtualdj.exe"
VDJ_PROCESS_PATH_MAC = "/Applications/VirtualDJ.app"
VDJ_PROCESS_SETTINGS = "settings.xml"

# VirtualDJ - Songs database
VDJ_XML_DATABASE_NAME = "database.xml"
VDJ_SQLITE_EXTRA_DB = "extra.db"
VDJ_SQLITE_EXTRA_DB_LYRICS = "lyrics"
VDJ_SQLITE_EXTRA_DB_RELATED_TRACKS = "related_tracks"
VDJ_SQLITE_EXTRA_DB_TRACK_DATA = "track_data"
VDJ_FOLDER_CACHE = 'Cache'
VDJ_SQLITE_CACHE_DB = "cache.db"
VDJ_SQLITE_CACHE_DB_WAVEFORMS = "waveforms"

# VirtualDJ - History
VDJ_FOLDER_HISTORY = 'History'
VDJ_TRACKLIST_FILENAME = "tracklist.txt"