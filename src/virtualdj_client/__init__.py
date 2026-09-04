__version__ = "1.0.1"

from .client import VirtualDJClient, VDJError
from .songs_database import VirtualDJSongsDatabase
from .history import VirtualDJHistory

from .client import __version__ as __client_version__
from .songs_database import __version__ as __songs_database_version__
from .history import __version__ as __history_version__

__all__ = ["__version__", "VirtualDJClient", "VDJError", "VirtualDJSongsDatabase","VirtualDJHistory","__client_version__","__songs_database_version__","__history_version__"]