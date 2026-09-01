__version__ = "1.0.0"

from .client import VirtualDJClient, VDJError
from .songs_database import VirtualDJSongsDatabase

from .client import __version__ as __client_version__
from .songs_database import __version__ as __songs_database_version__

__all__ = ["__version__", "VirtualDJClient", "VDJError", "VirtualDJSongsDatabase","__client_version__","__songs_database_version__"]