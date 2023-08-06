from base64 import b64encode
from typing import Dict

from pydantic import BaseModel

from nidhoggr_core.texture import TextureType, TextureItem
from nidhoggr_core.user import UserProperty
from nidhoggr.utils.transformer import JSONResponseTransformer


class TextureResponse(BaseModel, JSONResponseTransformer):
    timestamp: int
    profileId: str
    profileName: str
    textures: Dict[TextureType, TextureItem]

    class Config:
        allow_mutation = False
        use_enum_values = True

    def pack(self) -> UserProperty:
        return UserProperty(
            name="textures",
            value=b64encode(self.json().encode('ascii')).decode('ascii')
        )
