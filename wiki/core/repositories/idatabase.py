from __future__ import annotations
import abc


class IDatabase(metaclass=abc.ABCMeta):
    def __enter__(self) -> IDatabase:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

    @abc.abstractmethod
    def close(self) -> None:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def context(self):
        raise NotImplementedError()
