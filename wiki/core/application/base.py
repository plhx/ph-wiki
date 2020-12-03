from __future__ import annotations
import abc
import typing


class IApplicationRequest(metaclass=abc.ABCMeta):
    pass


class IApplicationResponse(metaclass=abc.ABCMeta):
    pass


class IApplicationHandler(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def execute(self, request: ApplicationRequest) -> ApplicationResponse:
        raise NotImplementedError()


class ApplicationInjector:
    def resolve(self, klass: typing.Type) -> typing.Any:
        return klass()


class ApplicationMediator:
    def __init__(self, injector: ApplicationInjector=None):
        self.injector = injector if injector else ApplicationInjector()
        self.handlers = {}

    def bind(self, request_class, handler_class) -> None:
        self.handlers[request_class] = handler_class

    def call(self, request: IApplicationRequest) -> IApplicationResponse:
        if not isinstance(request, IApplicationRequest):
            raise TypeError()
        handler = self.injector.resolve(self.handlers[type(request)])
        response = handler.execute(request)
        if not isinstance(response, IApplicationResponse):
            raise TypeError()
        return response
