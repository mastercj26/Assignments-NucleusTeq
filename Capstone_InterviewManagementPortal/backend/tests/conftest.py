# Tests run on mongomock (in-memory mongo), so no local MongoDB is needed.

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import mongomock
import mongomock.gridfs

mongomock.gridfs.enable_gridfs_integration()

from src.core.database import Database  # noqa: E402

Database.client = mongomock.MongoClient()
Database.db = Database.client["interview_portal_test"]
