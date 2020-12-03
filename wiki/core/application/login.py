from __future__ import annotations
from .base import *
from ..models.session import *
from ..repositories.isession_repository import *
from ..repositories.iuser_repository import *
from ...dependencies import *


class LoginRequest(IApplicationRequest):
    def __init__(self, user_id: UserId, password: UserPassword):
        self.user_id = user_id
        self.password = password


class LoginResponse(IApplicationResponse):
    def __init__(self, session_id: [SessionId], expires: [SessionExpires]):
        self.session_id = session_id
        self.expires = expires


class LoginHandler(IApplicationHandler):
    def __init__(self):
        self.user_repository = Dependency.resolve(IUserRepository)
        self.session_repository = Dependency.resolve(ISessionRepository)

    def execute(self, request: IApplicationRequest) -> IApplicationResponse:
        user = self.user_repository.load(request.user_id)
        if user is None:
            raise LookupError()
        hashed = UserHashedPassword.frompassword(request.password, user.secret)
        if user.password != hashed:
            raise ValueError()
        session = Session(
            session_id=SessionId.generate(),
            user_id=user.user_id,
            expires=SessionExpires( \
                datetime.datetime.now(datetime.timezone.utc) \
                    + datetime.timedelta(days=30)
            )
        )
        self.session_repository.save(session)
        self.session_repository.purge()
        return LoginResponse(
            session_id=session.session_id,
            expires=session.expires
        )
