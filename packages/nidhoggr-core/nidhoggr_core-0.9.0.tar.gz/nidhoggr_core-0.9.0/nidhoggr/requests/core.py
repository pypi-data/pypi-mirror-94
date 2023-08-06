from abc import ABCMeta
from typing import Union, TypeVar, Type

from pydantic import BaseModel, ValidationError
from requests import Session, RequestException

from nidhoggr.core.response import ErrorResponse

T = TypeVar('T', bound=BaseModel)


class RequestsRepo(metaclass=ABCMeta):
    _session: Session
    _api_url: str
    _timeout: int

    def __init__(self, *, api_url: str, bearer_token: str, timeout: int = 1):
        session = Session()
        session.headers.update({
            'Authorization': f'Bearer {bearer_token}',
            'Content-Type': 'application/json'
        })
        self._session = session
        self._api_url = api_url
        self._timeout = timeout

    def fetch(self, *, endpoint: str, payload: BaseModel, clazz: Type[T]) -> Union[ErrorResponse, T]:
        try:
            response = self._session.post(f'{self._api_url}{endpoint}', data=payload.json(), timeout=self._timeout)
        except RequestException as e:
            return ErrorResponse(reason=f"Failed to fetch {endpoint}", exception=e)

        if response.status_code != 200:
            return ErrorResponse(reason=f"Expected 200, got {response.status_code} for {endpoint}")

        result = response.json()
        if not result:
            return ErrorResponse(reason=f"Response from {endpoint} didn't contain valid JSON, but {response.text}")

        try:
            return clazz.parse_obj(result)
        except ValidationError as e:
            return ErrorResponse(reason=f"Received malformed {clazz} object from API, got {result}", exception=e)
