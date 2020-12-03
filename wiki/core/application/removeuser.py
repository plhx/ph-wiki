from .base import *
from ..repositories.iuser_repository import *
from ...dependencies import *


class RemoveUserRequest(IApplicationRequest):
    def __init__(self, requestor: User, user_id: UserId):
        self.requestor = requestor
        self.user_id = user_id


class RemoveUserResponse(IApplicationResponse):
    pass


class RemoveUserHandler(IApplicationHandler):
    def __init__(self):
        self.user_repository = Dependency.resolve(IUserRepository)

    def execute(self, request: IApplicationRequest) -> IApplicationResponse:
        if len(request.user_id.value) == 0:
            raise ValueError()
        user = self.user_repository.load(request.user_id)
        if request.requestor.role < user.role:
            raise ValueError()
        self.user_repository.remove(user)
        return RemoveUserResponse()
