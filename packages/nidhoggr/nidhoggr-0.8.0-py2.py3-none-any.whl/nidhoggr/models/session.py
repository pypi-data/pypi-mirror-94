from typing import Optional, List

from pydantic import BaseModel

from nidhoggr_core.user import UserProperty
from nidhoggr.utils.transformer import YggdrasilRequestTransformer, JSONResponseTransformer, LegacyRequestTransformer


class JoinRequest(BaseModel, YggdrasilRequestTransformer):
    accessToken: str
    selectedProfile: str
    serverId: str

    class Config:
        allow_mutation = False


class HasJoinedRequestBase(BaseModel):
    username: str
    serverId: str
    ip: Optional[str]


class HasJoinedRequest(HasJoinedRequestBase, YggdrasilRequestTransformer):

    class Config:
        allow_mutation = False


class HasJoinedRequestLegacy(HasJoinedRequestBase, LegacyRequestTransformer):

    class Config:
        allow_mutation = False


class JoinedResponse(BaseModel, JSONResponseTransformer):
    id: str
    name: str
    properties: List[UserProperty]

    class Config:
        allow_mutation = False


class ProfileRequestBase(BaseModel):
    id: str
    unsigned: bool = False

    class Config:
        allow_mutation = False


class ProfileRequest(ProfileRequestBase, YggdrasilRequestTransformer):

    class Config:
        allow_mutation = False


class ProfileRequestLegacy(ProfileRequestBase, LegacyRequestTransformer):

    class Config:
        allow_mutation = False
