from typing import Dict, Union
from uuid import UUID

from nidhoggr.core.repository import BaseUserRepo
from nidhoggr.core.response import StatusResponse, ErrorResponse
from nidhoggr.core.user import User, PasswordRequest, UserRequest
from nidhoggr.requests.core import RequestsRepo


class RequestsUserRepo(BaseUserRepo, RequestsRepo):

    def get_user(self, **kwargs: Dict[str, Union[str, UUID]]) -> Union[ErrorResponse, User]:
        payload = UserRequest(**kwargs)
        return self.fetch(endpoint='/user/get/', payload=payload, clazz=User)

    def check_password(self, *, clean: str, uuid: str) -> Union[ErrorResponse, StatusResponse]:
        payload = PasswordRequest(uuid=uuid, password=clean)
        return self.fetch(endpoint='/user/check_password/', payload=payload, clazz=StatusResponse)

    def save_user(self, *, user: User) -> Union[ErrorResponse, User]:
        return self.fetch(endpoint='/user/save/', payload=user, clazz=User)
