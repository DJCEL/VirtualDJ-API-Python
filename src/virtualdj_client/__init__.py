__version__ = "1.1.2"

from .client import VirtualDJClient
from .client_utils import VirtualDJClientUtils
from .client_songs_database import VirtualDJSongsDatabase
from .client_history_files import VirtualDJHistoryFiles

from .client import __version__ as __client_version__
from .client_utils import __version__ as __client_utils_version__
from .client_songs_database import __version__ as __client_songs_database_version__
from .client_history_files import __version__ as __client_history_files_version__

__all__ = ["__version__", "VirtualDJClient", "VirtualDJClientUtils", "VirtualDJSongsDatabase","VirtualDJHistoryFiles","__client_version__","__client_utils_version__","__client_songs_database_version__","__client_history_files_version__"]