__version__ = "1.1.3"

from .client import VirtualDJClient, VDJDeck
from .client_utils import VirtualDJUtils
from .client_settings import VirtualDJSettings
from .client_songs_database import VirtualDJSongsDatabase
from .client_history_files import VirtualDJHistoryFiles

from .client import __version__ as __client_version__
from .client_utils import __version__ as __client_utils_version__
from .client_settings import __version__ as __client_settings_version__
from .client_songs_database import __version__ as __client_songs_database_version__
from .client_history_files import __version__ as __client_history_files_version__

__all__ = ["__version__", 
           "VirtualDJClient", 
           "VDJDeck", 
           "VirtualDJUtils", 
           "VirtualDJSettings",
           "VirtualDJSongsDatabase",
           "VirtualDJHistoryFiles",
           "__client_version__",
           "__client_utils_version__",
           "__client_songs_database_version__",
           "__client_history_files_version__",
           "__client_settings_version__"
           ]