import datetime


__all__ = ['jstoffset']


class JSTOffset(datetime.tzinfo):
    def utcoffset(self, dt: datetime.datetime) -> datetime.timedelta:
        return datetime.timedelta(hours=9)

    def dst(self, dt: datetime.datetime) -> datetime.timedelta:
        return datetime.timedelta(0)

    def tzname(self) -> str:
        return 'Asia/Tokyo'


jstoffset = JSTOffset()
