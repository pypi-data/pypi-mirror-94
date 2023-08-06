from enum import Enum
from typing import Optional, Dict, List

from pydantic.main import BaseModel

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
    uuid: str
    texture_types: List[TextureType] = [TextureType.SKIN]

    class Config:
        allow_mutation = False


class TextureResponse(BaseModel):
    textures: Dict[TextureType, TextureItem]

    class Config:
        allow_mutation = False
