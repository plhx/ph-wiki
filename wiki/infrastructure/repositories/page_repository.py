import abc
import sqlite3
import typing
import injector
from ...core.models.page import *
from ...core.models.timezone import *
from ...core.repositories.idatabase import *
from ...core.repositories.ipage_repository import *


class PageRepository(IPageRepository):
    @injector.inject
    def __init__(self, database: IDatabase):
        self.database = database
        self._create()

    def _create(self):
        cur = self.database.context.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS [page] (
            [page_id] TEXT PRIMARY KEY,
            [page_title] TEXT NOT NULL,
            [page_body] TEXT NOT NULL,
            [page_lastmodified] TIMESTAMP NOT NULL,
            [page_version] INTEGER NOT NULL
        )''')
        self.database.context.commit()

    def load(self, page_id: PageId) -> typing.Union[Page, None]:
        cur = self.database.context.cursor()
        cur.execute('''SELECT [page_id], [page_title], [page_body],
            [page_lastmodified], [page_version] FROM [page]
            WHERE [page_id] = :page_id''',
            {'page_id': page_id.value}
        )
        row = cur.fetchone()
        if row is None:
            return None
        page_id, title, body, lastmodified, version = row
        return Page(
            page_id=PageId(page_id),
            title=PageTitle(title),
            body=PageBody(body),
            lastmodified=PageLastModified(
                lastmodified.astimezone(datetime.timezone.utc)
            ),
            version=PageVersion(version)
        )

    def loadall(self) -> [Page]:
        cur = self.database.context.cursor()
        cur.execute('''SELECT [page_id], [page_title], [page_body],
            [page_lastmodified], [page_version] FROM [page]''')
        result = []
        for page_id, title, body, lastmodified, version in cur.fetchall():
            page = Page(
                page_id=PageId(page_id),
                title=PageTitle(title),
                body=PageBody(body),
                lastmodified=PageLastModified(lastmodified),
                version=PageVersion(version)
            )
            result.append(page)
        return result

    def save(self, page: Page) -> None:
        cur = self.database.context.cursor()
        if sqlite3.sqlite_version_info < (3, 24, 0):
            p = self.load(page.page_id)
            if p is None:
                cur.execute('''INSERT INTO [page] ([page_id], [page_title],
                        [page_body], [page_lastmodified], [page_version])
                    VALUES (:page_id, :title, :body, :lastmodified, 0)''',
                    {k: v.value for k, v in page.__dict__.items()}
                )
            else:
                cur.execute('''UPDATE [page] SET
                        [page_title] = :title,
                        [page_body] = :body,
                        [page_lastmodified] = :lastmodified,
                        [page_version] = :version + 1
                    WHERE
                        [page_id] = :page_id AND [page_version] = :version''',
                    {k: v.value for k, v in page.__dict__.items()}
                )
        else:
            cur.execute('''INSERT INTO [page] ([page_id], [page_title],
                    [page_body], [page_lastmodified], [page_version])
                VALUES (:page_id, :title, :body, :lastmodified, 0)
                ON CONFLICT([page_id])
                DO UPDATE SET [page_title] = :title,
                    [page_body] = :body,
                    [page_lastmodified] = :lastmodified,
                    [page_version] = :version + 1
                    WHERE [page_version] = :version''',
                {k: v.value for k, v in page.__dict__.items()}
            )
        if cur.rowcount != 1:
            raise RuntimeError()
        self.database.context.commit()

    def remove(self, page: Page) -> None:
        cur = self.database.context.cursor()
        cur.execute(
            'DELETE FROM [page] WHERE [page_id] = :page_id',
            {k: v.value for k, v in page.__dict__.items()}
        )
        self.database.context.commit()
