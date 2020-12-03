from .base import *
from ..repositories.ipage_repository import *
from ...dependencies import *


class LoadPageRequest(IApplicationRequest):
    def __init__(self, page_id: PageId):
        self.page_id = page_id


class LoadPageResponse(IApplicationResponse):
    def __init__(self, page: Page):
        self.page = page


class LoadPageHandler(IApplicationHandler):
    def __init__(self):
        self.page_repository = Dependency.resolve(IPageRepository)

    def execute(self, request: IApplicationRequest) -> IApplicationResponse:
        page = self.page_repository.load(request.page_id)
        if page is None:
            page = Page(
                page_id=request.page_id,
                title=PageTitle(''),
                body=PageBody(''),
                lastmodified=PageLastModified(
                    datetime.datetime.now(datetime.timezone.utc)
                ),
                version=PageVersion(0)
            )
        return LoadPageResponse(page=page)
