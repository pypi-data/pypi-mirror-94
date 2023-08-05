from abc import ABCMeta, abstractmethod
from typing import Dict, Union

from nidhoggr_core.response import StatusResponse, ErrorResponse
from nidhoggr_core.texture import TextureType, TextureItem
from nidhoggr_core.user import User


class BaseTextureRepo(metaclass=ABCMeta):
    variant: str

    @abstractmethod
    def get(self, *, uuid: str) -> Union[ErrorResponse, Dict[TextureType, TextureItem]]:
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
