"""Account manager package for linked email account storage and pulling."""

from .service import AccountManagerService
from .storage import AccountStorage

__all__ = ["AccountManagerService", "AccountStorage"]
