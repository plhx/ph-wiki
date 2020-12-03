from __future__ import annotations
from ...core.repositories.idatabase import *
import sqlite3
import injector


class SQLite3Database(IDatabase):
    def __init__(self, path):
        self.path = path
        self._context = sqlite3.connect(
            path,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )

    def close(self) -> None:
        self._context.close()

    @property
    def context(self):
        return self._context
