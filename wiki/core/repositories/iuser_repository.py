from __future__ import annotations
import abc
from ..models.user import *


class IUserRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def load(self, user_id: UserId) -> User:
        raise NotImplementedError()

    @abc.abstractmethod
    def loadall(self) -> [User]:
        raise NotImplementedError()

    @abc.abstractmethod
    def save(self, user: User) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def remove(self, user: User) -> None:
        raise NotImplementedError()
