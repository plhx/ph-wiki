from __future__ import annotations
import abc
from typing import Union
from ..models.page import *


class IPageRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def load(self, page_id: PageId) -> Union[Page, None]:
        raise NotImplementedError()

    @abc.abstractmethod
    def loadall(self) -> [Page]:
        raise NotImplementedError()

    @abc.abstractmethod
    def save(self, page: Page) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def remove(self, page: Page) -> None:
        raise NotImplementedError()
