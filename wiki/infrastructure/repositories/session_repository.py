import datetime
import typing
import injector
from ...core.models.session import *
from ...core.models.user import *
from ...core.models.timezone import *
from ...core.repositories.idatabase import *
from ...core.repositories.isession_repository import *


class SessionRepository(ISessionRepository):
    @injector.inject
    def __init__(self, database: IDatabase):
        self.database = database
        self._create()

    def _create(self):
        cur = self.database.context.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS [session] (
            [session_id] TEXT PRIMARY KEY,
            [user_id] TEXT NOT NULL,
            [expires] TIMESTAMP NOT NULL
        )''')
        self.database.context.commit()

    def load(self, session_id: SessionId) -> typing.Union[Session, None]:
        cur = self.database.context.cursor()
        cur.execute('''SELECT [session_id], [user_id], [expires]
            FROM [session]
            WHERE [session_id] = :session_id AND [expires] > :now''',
            {
                'session_id': session_id.value,
                'now': datetime.datetime.now(datetime.timezone.utc)
            }
        )
        row = cur.fetchone()
        if row is None:
            return None
        session_id, user_id, expires = row
        return Session(
            session_id=SessionId(session_id),
            user_id=UserId(user_id),
            expires=SessionExpires(expires.astimezone(datetime.timezone.utc))
        )

    def save(self, session: Session) -> None:
        cur = self.database.context.cursor()
        cur.execute('''REPLACE INTO [session]
            ([session_id], [user_id], [expires]) VALUES
            (:session_id, :user_id, :expires)''',
            {k: v.value for k, v in session.__dict__.items()}
        )
        self.database.context.commit()

    def purge(self) -> None:
        cur = self.database.context.cursor()
        cur.execute(
            'DELETE FROM [session] WHERE expires < :now',
            {'now': datetime.datetime.utcnow()}
        )
        self.database.context.commit()
