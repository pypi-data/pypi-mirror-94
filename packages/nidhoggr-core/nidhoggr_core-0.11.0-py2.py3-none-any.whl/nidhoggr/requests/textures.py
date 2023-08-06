from typing import Union

from nidhoggr.core.repository import BaseTextureRepo
from nidhoggr.core.response import ErrorResponse, TextureStatusResponse
from nidhoggr.core.texture import TextureRequest, SimpleTextureResponse, TextureUploadRequest
from nidhoggr.requests.core import RequestsRepo


class RequestsTextureRepo(BaseTextureRepo, RequestsRepo):

    def get(self, *, request: TextureRequest) -> Union[ErrorResponse, SimpleTextureResponse]:
        return self.fetch(endpoint='/texture/get/', payload=request, clazz=SimpleTextureResponse)

    def upload(self, *, request: TextureUploadRequest) -> Union[ErrorResponse, TextureStatusResponse]:
        return self.fetch(endpoint='/texture/upload/', payload=request, clazz=TextureStatusResponse)

    def clear(self, *, request: TextureRequest) -> Union[ErrorResponse, TextureStatusResponse]:
        return self.fetch(endpoint='/texture/clear/', payload=request, clazz=TextureStatusResponse)
