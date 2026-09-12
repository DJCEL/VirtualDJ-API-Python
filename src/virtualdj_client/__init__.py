__version__ = "1.1.4"

from .client import VirtualDJClient
from .client_utils import VirtualDJUtils
from .client_settings import VirtualDJSettings
from .client_songs_database import VirtualDJSongsDatabase
from .client_history_files import VirtualDJHistoryFiles
from .clientExt import VirtualDJClientExt, VDJDeck, VdjDeckData

from .client import __version__ as __client_version__
from .client_utils import __version__ as __client_utils_version__
from .client_settings import __version__ as __client_settings_version__
from .client_songs_database import __version__ as __client_songs_database_version__
from .client_history_files import __version__ as __client_history_files_version__
from .clientExt import __version__ as __clientExt_version__

__all__ = [
    "__version__", 
    "VirtualDJClient", 
    "VirtualDJClientExt",
    "VDJDeck", 
    "VdjDeckData",
    "VirtualDJUtils", 
    "VirtualDJSettings",
    "VirtualDJSongsDatabase",
    "VirtualDJHistoryFiles",
    "__client_version__",
    "__client_utils_version__",
    "__client_songs_database_version__",
    "__client_history_files_version__",
    "__client_settings_version__",
    "__clientExt_version__"
]