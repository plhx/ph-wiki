from .base import *
from ..repositories.iuser_repository import *
from ...dependencies import *


class SaveProfileRequest(IApplicationRequest):
    def __init__(self, user_id: UserId, name: UserName,
        password: UserPassword, retypepassword: UserPassword):
        self.user_id = user_id
        self.name = name
        self.password = password
        self.retypepassword = retypepassword


class SaveProfileResponse(IApplicationResponse):
    pass


class SaveProfileHandler(IApplicationHandler):
    def __init__(self):
        self.user_repository = Dependency.resolve(IUserRepository)

    def execute(self, request: IApplicationRequest) -> IApplicationResponse:
        user = self.user_repository.load(request.user_id)
        if user is None:
            raise LookupError()
        if len(request.name.value) > 0:
            user.name = request.name
        if len(request.password.value) == 0:
            pass
        elif len(request.password.value) < 4:
            raise ValueError()
        else:
            if request.password != request.retypepassword:
                raise ValueError()
            user.password = UserHashedPassword.frompassword(
                request.password,
                UserSecret.generate()
            )
        self.user_repository.save(user)
        return SaveProfileResponse()
