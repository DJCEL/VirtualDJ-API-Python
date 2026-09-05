__version__ = "1.1.0"

from .client import VirtualDJClient, VDJError
from .songs_database import VirtualDJSongsDatabase
from .history_files import VirtualDJHistoryFiles

from .client import __version__ as __client_version__
from .songs_database import __version__ as __songs_database_version__
from .history_files import __version__ as __history_files_version__

__all__ = ["__version__", "VirtualDJClient", "VDJError", "VirtualDJSongsDatabase","VirtualDJHistoryFiles","__client_version__","__songs_database_version__","__history_files_version__"]