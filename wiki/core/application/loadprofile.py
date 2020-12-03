from .base import *
from ..repositories.iuser_repository import *
from ...dependencies import *


class LoadProfileRequest(IApplicationRequest):
    def __init__(self, user_id: UserId):
        self.user_id = user_id


class LoadProfileResponse(IApplicationResponse):
    def __init__(self, user: User):
        self.user = user


class LoadProfileHandler(IApplicationHandler):
    def __init__(self):
        self.user_repository = Dependency.resolve(IUserRepository)

    def execute(self, request: IApplicationRequest) -> IApplicationResponse:
        user = self.user_repository.load(request.user_id)
        return LoadProfileResponse(user=user)
