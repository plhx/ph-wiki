import enum
import hashlib
import hmac
import secrets
from .model import IEntity, IValueObject


class UserId(IValueObject):
    def __init__(self, value: str):
        if not isinstance(value, str):
            raise TypeError(value)
        self.value = value


class UserName(IValueObject):
    def __init__(self, value: str):
        if not isinstance(value, str):
            raise TypeError(value)
        self.value = value


class UserPassword(IValueObject):
    def __init__(self, value: str):
        if not isinstance(value, str):
            raise TypeError(value)
        self.value = value


class UserSecret(IValueObject):
    def __init__(self, value: bytes):
        if not isinstance(value, (bytes, bytearray)):
            raise TypeError(value)
        self.value = value

    @classmethod
    def generate(cls, length=32):
        return cls(secrets.token_bytes(length))


class UserHashedPassword(IValueObject):
    def __init__(self, value: str):
        if not isinstance(value, str):
            raise TypeError(value)
        self.value = value

    @classmethod
    def frompassword(cls, password: UserPassword, secret: UserSecret):
        hashed = hmac.HMAC(
            secret.value,
            password.value.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return cls(hashed)


class UserRole(enum.IntEnum):
    NONE          = 0
    WRITER        = 1
    ADMINISTRATOR = 1000


class User(IEntity):
    def __init__(self, user_id: UserId, name: UserName,
        password: UserHashedPassword, secret: UserSecret, role: UserRole):
        if not isinstance(user_id, UserId):
            raise TypeError(user_id)
        if not isinstance(name, UserName):
            raise TypeError(name)
        if not isinstance(password, UserHashedPassword):
            raise TypeError(password)
        if not isinstance(secret, UserSecret):
            raise TypeError(secret)
        if not isinstance(role, UserRole):
            raise TypeError(role)
        self.user_id = user_id
        self.name = name
        self.password = password
        self.secret = secret
        self.role = role

    @property
    def identity(self) -> str:
        return self.user_id.value
