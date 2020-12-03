from __future__ import annotations
from wiki.core.application.base import *
from wiki.core.application.getusers import *
from wiki.core.application.adduser import *
from wiki.core.application.updateuser import *
from wiki.core.application.removeuser import *
from wiki.core.application.login import *
from wiki.core.application.loadpage import *
from wiki.core.application.savepage import *
from wiki.core.application.loadprofile import *
from wiki.core.application.saveprofile import *


__all__ = ['Service']


Service = ApplicationMediator()

Service.bind(GetUsersRequest, GetUsersHandler)
Service.bind(AddUserRequest, AddUserHandler)
Service.bind(UpdateUserRequest, UpdateUserHandler)
Service.bind(RemoveUserRequest, RemoveUserHandler)

Service.bind(LoginRequest, LoginHandler)

Service.bind(LoadPageRequest, LoadPageHandler)
Service.bind(SavePageRequest, SavePageHandler)

Service.bind(LoadProfileRequest, LoadProfileHandler)
Service.bind(SaveProfileRequest, SaveProfileHandler)
