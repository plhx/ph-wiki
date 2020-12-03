from __future__ import annotations
import datetime
import uuid
from .model import *
from .user import *


class SessionId(IValueObject):
    def __init__(self, value: str):
        if not isinstance(value, str):
            raise TypeError(value)
        self.value = value

    @classmethod
    def generate(cls):
        return cls(str(uuid.uuid4()))


class SessionExpires(IValueObject):
    def __init__(self, value: datetime.datetime):
        if not isinstance(value, datetime.datetime):
            raise TypeError(value)
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            raise ValueError(value)
        self.value = value

    def __lt__(self, other) -> bool:
        if type(self) != type(other):
            raise TypeError(other)
        return self.value < other.value

    def __gt__(self, other) -> bool:
        if type(self) != type(other):
            raise TypeError(other)
        return self.value > other.value


class Session(IEntity):
    def __init__(self, \
        session_id: SessionId, user_id: UserId, expires: SessionExpires):
        if not isinstance(session_id, SessionId):
            raise TypeError(session_id)
        if not isinstance(user_id, UserId):
            raise TypeError(user_id)
        if not isinstance(expires, SessionExpires):
            raise TypeError(expires)
        self.session_id = session_id
        self.user_id = user_id
        self.expires = expires

    @property
    def identity(self) -> str:
        return self.session_id.value
