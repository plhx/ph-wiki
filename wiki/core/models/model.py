import abc
import typing


class IValueObject(metaclass=abc.ABCMeta):
    def __repr__(self) -> str:
        return repr(self.value)

    def __eq__(self, other: typing.Any) -> bool:
        return type(self) == type(other) and self.value == other.value


class IEntity(metaclass=abc.ABCMeta):
    def __repr__(self) -> str:
        return repr(self.__dict__)

    def __eq__(self, other: typing.Any) -> bool:
        return type(self) == type(other) and self.identity == other.identity

    @property
    @abc.abstractmethod
    def identity(self) -> str:
        raise NotImplementedError()
