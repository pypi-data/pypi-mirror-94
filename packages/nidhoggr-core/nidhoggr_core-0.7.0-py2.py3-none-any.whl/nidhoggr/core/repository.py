from abc import ABCMeta, abstractmethod
from typing import Dict, Union

from nidhoggr.core.response import StatusResponse, TextureStatusResponse, ErrorResponse
from nidhoggr.core.texture import TextureType, TextureItem, TextureUploadRequest, TextureRequest
from nidhoggr.core.user import User


class BaseTextureRepo(metaclass=ABCMeta):
    variant: str

    @abstractmethod
    def get(self, *, request: TextureRequest) -> Union[ErrorResponse, Dict[TextureType, TextureItem]]:
        pass

    @abstractmethod
    def upload(self, *, request: TextureUploadRequest) -> Union[ErrorResponse, TextureStatusResponse]:
        pass

    @abstractmethod
    def clear(self, *, request: TextureRequest) -> Union[ErrorResponse, TextureStatusResponse]:
        pass


class BaseUserRepo(metaclass=ABCMeta):
    EMPTY_USER = User(
        uuid="00000000000000000000000000000000",
        login="empty",
        email="empty@example.com",
        synthetic=True
    )

    @abstractmethod
    def get_user(self, **kw: Dict[str, str]) -> Union[ErrorResponse, User]:
        pass

    @abstractmethod
    def check_password(self, *, clean: str, uuid: str) -> Union[ErrorResponse, StatusResponse]:
        pass

    @abstractmethod
    def save_user(self, *, user: User) -> Union[ErrorResponse, User]:
        pass
