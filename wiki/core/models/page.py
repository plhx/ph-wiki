import datetime
from .model import IEntity, IValueObject


class PageId(IValueObject):
    def __init__(self, value: str):
        if not isinstance(value, str):
            raise TypeError(value)
        self.value = value


class PageTitle(IValueObject):
    def __init__(self, value: str):
        if not isinstance(value, str):
            raise TypeError(value)
        self.value = value


class PageBody(IValueObject):
    def __init__(self, value: str):
        if not isinstance(value, str):
            raise TypeError(value)
        self.value = value


class PageLastModified(IValueObject):
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

    @classmethod
    def now(cls) -> 'PageLastModified':
        return cls(datetime.datetime.now(datetime.timezone.utc))


class PageVersion(IValueObject):
    def __init__(self, value: int):
        if not isinstance(value, int):
            raise TypeError(value)
        self.value = value

    def __lt__(self, other) -> bool:
        if type(self) != type(other):
            raise TypeError(other)
        return self.value < other.value

    def __gt__(self, other) -> bool:
        if type(self) != type(other):
            raise TypeError(other)
        return self.value > other.value


class Page(IEntity):
    def __init__(self, page_id: PageId, title: PageTitle, body: PageBody, \
        lastmodified: PageLastModified, version: PageVersion):
        if not isinstance(page_id, PageId):
            raise TypeError(page_id)
        if not isinstance(title, PageTitle):
            raise TypeError(title)
        if not isinstance(body, PageBody):
            raise TypeError(body)
        if not isinstance(lastmodified, PageLastModified):
            raise TypeError(lastmodified)
        if not isinstance(version, PageVersion):
            raise TypeError(version)
        self.page_id = page_id
        self.title = title
        self.body = body
        self.lastmodified = lastmodified
        self.version = version

    @property
    def identity(self) -> str:
        return self.page_id.value
