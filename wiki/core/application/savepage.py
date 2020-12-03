from __future__ import annotations
from .base import *
from ..repositories.ipage_repository import *
from ...dependencies import *


class SavePageRequest(IApplicationRequest):
    def __init__(self, page: Page):
        self.page = page


class SavePageResponse(IApplicationResponse):
    pass


class SavePageHandler(IApplicationHandler):
    def __init__(self):
        self.page_repository = Dependency.resolve(IPageRepository)

    def execute(self, request: IApplicationRequest) -> IApplicationResponse:
        if request.page.body.value:
            self.page_repository.save(request.page)
        else:
            self.page_repository.remove(request.page)
        return SavePageResponse()
