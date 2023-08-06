from typing import Optional, List

from pydantic import UUID4
from pydantic.main import BaseModel


class UserProperty(BaseModel):
    name: str
    value: str
    signature: Optional[str] = None

    class Config:
        allow_mutation = False
        ignore_extra = False

    def __hash__(self):
        return hash((self.name, self.value, self.signature))

    @property
    def unsigned(self):
        return self.copy(update=dict(signature=None))


class User(BaseModel):
    uuid: UUID4
    login: str
    email: str
    access: Optional[UUID4] = None
    client: Optional[UUID4] = None
    server: Optional[str] = None
    properties: List[UserProperty] = []
    synthetic: bool = False

    class Config:
        allow_mutation = False


class UserRequest(BaseModel):
    uuid: Optional[UUID4] = None
    login: Optional[str] = None
    email: Optional[str] = None
    access: Optional[UUID4] = None
    client: Optional[UUID4] = None
    server: Optional[str] = None

    class Config:
        allow_mutation = False


class PasswordRequest(BaseModel):
    uuid: UUID4
    password: str

    class Config:
        allow_mutation = False
