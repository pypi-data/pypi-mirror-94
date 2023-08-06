from base64 import b64encode
from enum import Enum
from typing import Optional, Dict, List

from pydantic import UUID4
from pydantic.main import BaseModel

from nidhoggr.core.user import UserProperty

TextureMeta = Optional[Dict[str, str]]


class TextureType(Enum):
    SKIN = "SKIN"
    CAPE = "CAPE"
    ELYTRA = "ELYTRA"


class TextureItem(BaseModel):
    url: str
    metadata: TextureMeta = None

    class Config:
        allow_mutation = False


class TextureRequest(BaseModel):
    uuid: UUID4
    texture_types: List[TextureType] = [TextureType.SKIN]

    class Config:
        allow_mutation = False


class TextureUploadRequest(BaseModel):
    uuid: UUID4
    data: str
    kind: TextureType
    metadata: TextureMeta

    class Config:
        allow_mutation = False


class SimpleTextureResponse(BaseModel):
    textures: Dict[TextureType, TextureItem]

    class Config:
        allow_mutation = False
        use_enum_values = True


class ComplexTextureResponse(SimpleTextureResponse):
    timestamp: int
    profileId: UUID4
    profileName: str

    class Config:
        allow_mutation = False
        use_enum_values = True

    def pack(self) -> UserProperty:
        return UserProperty(
            name="textures",
            value=b64encode(self.json().encode('ascii')).decode('ascii')
        )
