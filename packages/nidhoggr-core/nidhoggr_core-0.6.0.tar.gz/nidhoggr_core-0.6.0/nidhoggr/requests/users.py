from typing import Dict, Union, Any

from pydantic.error_wrappers import ValidationError

from nidhoggr.core.repository import BaseUserRepo
from nidhoggr.core.response import StatusResponse, ErrorResponse
from nidhoggr.core.user import User

from nidhoggr.requests.core import RequestsRepo


class RequestsUserRepo(BaseUserRepo, RequestsRepo):

    @staticmethod
    def _parse_user(result: Dict[str, Any]) -> Union[ErrorResponse, User]:
        try:
            return User.parse_obj(result)
        except ValidationError as e:
            return ErrorResponse(reason="Received malformed User object from API", exception=e)

    def get_user(self, **kwargs: Dict[str, str]) -> Union[ErrorResponse, User]:
        result = self.fetch(endpoint='/user/get', payload=kwargs)

        if isinstance(result, ErrorResponse):
            return result

        return self._parse_user(result)

    def check_password(self, *, clean: str, uuid: str) -> Union[ErrorResponse, StatusResponse]:
        payload = {'uuid': uuid, 'password': clean}
        result = self.fetch(endpoint='/user/check_password', payload=payload)

        if isinstance(result, ErrorResponse):
            return result

        return StatusResponse(**result)

    def save_user(self, *, user: User) -> Union[ErrorResponse, User]:
        payload = user.dict()
        result = self.fetch(endpoint='/user/save', payload=payload)

        if isinstance(result, ErrorResponse):
            return result

        return self._parse_user(result)
