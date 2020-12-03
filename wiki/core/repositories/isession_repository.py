import abc
from typing import Union
from ..models.session import *
from ..models.user import *


class ISessionRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def load(self, session_id: SessionId) -> Union[Session, None]:
        raise NotImplementedError()

    @abc.abstractmethod
    def save(self, session: Session) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def purge(self) -> None:
        raise NotImplementedError()
