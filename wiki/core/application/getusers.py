from __future__ import annotations
from .base import *
from ..repositories.iuser_repository import *
from ...dependencies import *


class GetUsersRequest(IApplicationRequest):
    def __init__(self, user: User):
        self.user = user


class GetUsersResponse(IApplicationResponse):
    def __init__(self, users: [User], roles: [UserRole]):
        self.users = users
        self.roles = roles


class GetUsersHandler(IApplicationHandler):
    def __init__(self):
        self.user_repository = Dependency.resolve(IUserRepository)

    def execute(self, request: IApplicationRequest) -> IApplicationResponse:
        return GetUsersResponse(
            users=[user for user in self.user_repository.loadall()
                if user.role <= request.user.role],
            roles=[role for role in UserRole if role <= request.user.role]
        )
