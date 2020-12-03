import typing
import injector
from wiki.core.application.base import *
from wiki.core.repositories.idatabase import *
from wiki.core.repositories.ipage_repository import *
from wiki.core.repositories.isession_repository import *
from wiki.core.repositories.iuser_repository import *
from wiki.infrastructure.repositories.sqlite3_database import *
from wiki.infrastructure.repositories.page_repository import *
from wiki.infrastructure.repositories.session_repository import *
from wiki.infrastructure.repositories.user_repository import *


__all__ = ['Dependency']


class DependencyConfigure:
    def __init__(self):
        self.injector = injector.Injector(self.__class__.configure)

    @classmethod
    def configure(self, binder):
        binder.bind(
            IDatabase,
            to=injector.CallableProvider(lambda: SQLite3Database('wiki.db'))
        )
        binder.bind(IPageRepository, to=PageRepository)
        binder.bind(ISessionRepository, to=SessionRepository)
        binder.bind(IUserRepository, to=UserRepository)


class DependencyInjector(ApplicationInjector):
    def __init__(self):
        self.dependency = DependencyConfigure()

    def resolve(self, klass: typing.Type) -> typing.Any:
        return self.dependency.injector.get(klass)


Dependency = DependencyInjector()
