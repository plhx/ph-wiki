from __future__ import annotations
import injector
from ...core.models.user import *
from ...core.repositories.idatabase import *
from ...core.repositories.iuser_repository import *


class UserRepository(IUserRepository):
    @injector.inject
    def __init__(self, database: IDatabase):
        self.database = database
        self._create()

    def _create(self):
        cur = self.database.context.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS [user] (
            [user_id] TEXT PRIMARY KEY,
            [name] TEXT NOT NULL,
            [password] TEXT NOT NULL,
            [secret] BLOB NOT NULL,
            [role] INTEGER NOT NULL
        )''')
        secret = UserSecret.generate()
        password = UserPassword('root')
        password_hashed = UserHashedPassword.frompassword(password, secret)
        cur.execute('''INSERT INTO [user]
            ([user_id], [name], [password], [secret], [role])
                SELECT :user_id, :name, :password, :secret, :role
                WHERE (SELECT COUNT(*) FROM [user]) = 0''',
            {
                'user_id': 'root',
                'name': 'root',
                'password': password_hashed.value,
                'secret': secret.value,
                'role': UserRole.ADMINISTRATOR.value,
            }
        )
        self.database.context.commit()

    def load(self, user_id: UserId) -> User:
        cur = self.database.context.cursor()
        cur.execute('''SELECT [user_id], [name], [password], [secret], [role]
            FROM [user] WHERE [user_id] = :user_id''',
            {'user_id': user_id.value}
        )
        row = cur.fetchone()
        if row is None:
            return None
        user_id, name, password, secret, role = row
        return User(
            user_id=UserId(user_id),
            name=UserName(name),
            password=UserHashedPassword(password),
            secret=UserSecret(secret),
            role=UserRole(role)
        )

    def loadall(self) -> [User]:
        cur = self.database.context.cursor()
        cur.execute('''SELECT [user_id], [name], [password], [secret], [role]
        FROM [user]''')
        result = []
        for user_id, name, password, secret, role in cur.fetchall():
            user = User(
                user_id=UserId(user_id),
                name=UserName(name),
                password=UserHashedPassword(password),
                secret=UserSecret(secret),
                role=UserRole(role)
            )
            result.append(user)
        return result

    def save(self, user: User) -> None:
        cur = self.database.context.cursor()
        cur.execute('''INSERT INTO [user]
            ([user_id], [name], [password], [secret], [role]) VALUES
            (:user_id, :name, :password, :secret, :role)
            ON CONFLICT([user_id])
            DO UPDATE SET [name] = :name, [password] = :password,
                [secret] = :secret, [role] = :role''',
            {k: v.value for k, v in user.__dict__.items()}
        )
        self.database.context.commit()

    def remove(self, user: User) -> None:
        cur = self.database.context.cursor()
        cur.execute(
            'DELETE FROM [user] WHERE [user_id] = :user_id',
            {k: v.value for k, v in user.__dict__.items()}
        )
        self.database.context.commit()
