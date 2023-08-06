from typing import Optional

from pydantic import BaseModel


class StatusResponse(BaseModel):
    status: bool = True

    class Config:
        allow_mutation = False


class ErrorResponse(BaseModel):
    reason: str
    exception: Optional[str] = None

    class Config:
        allow_mutation = False


class TextureStatusResponse(BaseModel):
    message: str

    class Config:
        allow_mutation = False
