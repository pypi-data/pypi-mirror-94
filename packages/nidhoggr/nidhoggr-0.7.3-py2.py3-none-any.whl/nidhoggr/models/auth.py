from typing import List, Optional

from pydantic import BaseModel

from nidhoggr_core.user import UserProperty
from nidhoggr.utils.transformer import YggdrasilRequestTransformer, JSONResponseTransformer, EmptyResponseTransformer


class Agent(BaseModel):
    name: str = 'Minecraft'
    version: int = 1

    class Config:
        allow_mutation = False


class Profile(BaseModel):
    id: str
    name: str
    legacy: bool = False

    class Config:
        allow_mutation = False


class UserInstance(BaseModel):
    id: str
    properties: List[UserProperty] = []

    class Config:
        allow_mutation = False


class AuthenticationRequest(BaseModel, YggdrasilRequestTransformer):
    agent: Optional[Agent] = None
    username: str
    password: str
    clientToken: Optional[str] = None
    requestUser: bool = False

    class Config:
        allow_mutation = False


class AuthenticationResponse(BaseModel, JSONResponseTransformer):
    accessToken: str
    clientToken: str
    availableProfiles: Optional[List[Profile]] = None
    selectedProfile: Optional[Profile] = None
    user: Optional[UserInstance]

    class Config:
        allow_mutation = False


class RefreshRequest(BaseModel, YggdrasilRequestTransformer):
    accessToken: str
    clientToken: str
    selectedProfile: Optional[Profile] = None
    requestUser: bool = False

    class Config:
        allow_mutation = False


class RefreshResponse(BaseModel, JSONResponseTransformer):
    accessToken: str
    clientToken: str
    selectedProfile: Profile = None
    user: Optional[UserInstance] = None

    class Config:
        allow_mutation = False


class InvalidateRequest(BaseModel, YggdrasilRequestTransformer):
    accessToken: str
    clientToken: str

    class Config:
        allow_mutation = False


class SignOutRequest(BaseModel, YggdrasilRequestTransformer):
    username: str
    password: str

    class Config:
        allow_mutation = False


class ValidateRequest(BaseModel, YggdrasilRequestTransformer):
    accessToken: str
    clientToken: Optional[str] = None

    class Config:
        allow_mutation = False


class EmptyResponse(EmptyResponseTransformer):
    pass


NoContent = EmptyResponse()
