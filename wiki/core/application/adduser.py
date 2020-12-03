import re
from .base import *
from ..repositories.iuser_repository import *
from ...dependencies import *


class AddUserRequest(IApplicationRequest):
    def __init__(self, requestor: User, user_id: UserId, name: UserName, \
        password: UserPassword, role: UserRole):
        self.requestor = requestor
        self.user_id = user_id
        self.name = name
        self.password = password
        self.role = role


class AddUserResponse(IApplicationResponse):
    pass


class AddUserHandler(IApplicationHandler):
    def __init__(self):
        self.user_repository = Dependency.resolve(IUserRepository)

    def execute(self, request: IApplicationRequest) -> IApplicationResponse:
        if not re.match(r'[\w-]+', request.user_id.value):
            raise ValueError()
        if len(request.name.value) == 0:
            raise ValueError()
        if len(request.password.value) < 8:
            raise ValueError()
        if request.requestor.role < request.role:
            raise ValueError()
        secret = UserSecret.generate()
        user = User(
            user_id=request.user_id,
            name=request.name,
            password=UserHashedPassword.frompassword(request.password, secret),
            secret=secret,
            role=request.role
        )
        self.user_repository.save(user)
        return AddUserResponse()
