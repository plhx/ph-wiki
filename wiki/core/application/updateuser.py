from __future__ import annotations
from .base import *
from ..repositories.iuser_repository import *
from ...dependencies import *


class UpdateUserRequest(IApplicationRequest):
    def __init__(self, requestor: User, user_id: UserId, name: UserName, \
        role: UserRole):
        self.requestor = requestor
        self.user_id = user_id
        self.name = name
        self.role = role


class UpdateUserResponse(IApplicationResponse):
    pass


class UpdateUserHandler(IApplicationHandler):
    def __init__(self):
        self.user_repository = Dependency.resolve(IUserRepository)

    def execute(self, request: IApplicationRequest) -> IApplicationResponse:
        if len(request.name.value) == 0:
            raise ValueError()
        if request.requestor.role < request.role:
            raise ValueError()
        user = self.user_repository.load(request.user_id)
        user.name = request.name
        user.role = request.role
        self.user_repository.save(user)
        return UpdateUserResponse()
