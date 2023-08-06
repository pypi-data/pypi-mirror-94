from typing import Dict, Union

from nidhoggr.core.repository import BaseTextureRepo
from nidhoggr.core.response import ErrorResponse
from nidhoggr.core.texture import TextureType, TextureItem

from nidhoggr.requests.core import RequestsRepo


class RequestsTextureRepo(BaseTextureRepo, RequestsRepo):

    def get(self, *, uuid: str) -> Union[ErrorResponse, Dict[TextureType, TextureItem]]:
        payload = {'uuid': uuid}
        result = self.fetch(endpoint='/texture/get', payload=payload)

        if isinstance(result, ErrorResponse):
            return result

        return {
            TextureType(kind): TextureItem(url=url)
            for kind, url
            in result.items()
        }
