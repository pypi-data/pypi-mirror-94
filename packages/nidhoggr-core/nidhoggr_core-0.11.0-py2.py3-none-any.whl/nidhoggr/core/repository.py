from abc import ABCMeta, abstractmethod
from typing import Dict, Union
from uuid import UUID

from nidhoggr.core.response import StatusResponse, TextureStatusResponse, ErrorResponse
from nidhoggr.core.texture import TextureUploadRequest, TextureRequest, SimpleTextureResponse
from nidhoggr.core.user import User


class BaseTextureRepo(metaclass=ABCMeta):
    variant: str

    @abstractmethod
    def get(self, *, request: TextureRequest) -> Union[ErrorResponse, SimpleTextureResponse]:
        pass

    @abstractmethod
    def upload(self, *, request: TextureUploadRequest) -> Union[ErrorResponse, TextureStatusResponse]:
        pass

    @abstractmethod
    def clear(self, *, request: TextureRequest) -> Union[ErrorResponse, TextureStatusResponse]:
        pass


class BaseUserRepo(metaclass=ABCMeta):
    EMPTY_USER = User(
        uuid="8de67985-09c5-443b-be60-8fa552560e0e",
        login="empty",
        email="empty@example.com",
        synthetic=True
    )

    @abstractmethod
    def get_user(self, **kw: Dict[str, Union[str, UUID]]) -> Union[ErrorResponse, User]:
        pass

    @abstractmethod
    def check_password(self, *, clean: str, uuid: str) -> Union[ErrorResponse, StatusResponse]:
        pass

    @abstractmethod
    def save_user(self, *, user: User) -> Union[ErrorResponse, User]:
        pass
