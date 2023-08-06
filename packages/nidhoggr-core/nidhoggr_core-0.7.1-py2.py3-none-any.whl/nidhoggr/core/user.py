from typing import Optional, List

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
    uuid: str
    login: str
    email: str
    access: Optional[str] = None
    client: Optional[str] = None
    server: Optional[str] = None
    properties: List[UserProperty] = []
    synthetic: bool = False

    class Config:
        allow_mutation = False


class UserRequest(BaseModel):
    uuid: Optional[str] = None
    login: Optional[str] = None
    email: Optional[str] = None
    access: Optional[str] = None
    client: Optional[str] = None
    server: Optional[str] = None

    class Config:
        allow_mutation = False


class PasswordRequest(BaseModel):
    uuid: str
    password: str

    class Config:
        allow_mutation = False
