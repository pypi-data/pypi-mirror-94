from datetime import datetime
from typing import Union

from nidhoggr_core.config import BLConfig
from nidhoggr_core.repository import BaseTextureRepo, BaseUserRepo
from nidhoggr_core.user import User

from nidhoggr.errors.auth import InvalidProfile
from nidhoggr.errors.common import YggdrasilError
from nidhoggr.errors.session import InvalidServer
from nidhoggr.models.auth import EmptyResponse, NoContent
from nidhoggr.models.session import JoinRequest, HasJoinedRequest, JoinedResponse, ProfileRequest
from nidhoggr.models.texture import TextureResponse
from nidhoggr.utils.crypto import sign_property
from nidhoggr.utils.decorator import typed
from nidhoggr.utils.repository import handle_status


@typed
def join(req: JoinRequest, users: BaseUserRepo) -> Union[EmptyResponse, YggdrasilError]:
    user: User = handle_status(users.get_user(access=req.accessToken))

    if user.synthetic:
        return InvalidProfile

    if req.selectedProfile != user.uuid:
        return InvalidProfile

    user = user.copy(update=dict(server=req.serverId))
    handle_status(users.save_user(user=user))
    return NoContent


@typed
def has_joined(req: HasJoinedRequest, users: BaseUserRepo) -> Union[JoinedResponse, YggdrasilError]:
    user: User = handle_status(users.get_user(login=req.username))

    if user.synthetic:
        return InvalidProfile

    if req.serverId != user.server:
        return InvalidServer

    return JoinedResponse(
        id=user.uuid,
        name=user.login,
        properties=user.properties
    )


@typed
def profile(
    req: ProfileRequest,
    users: BaseUserRepo,
    config: BLConfig,
    textures: BaseTextureRepo
) -> Union[JoinedResponse, YggdrasilError]:
    user: User = handle_status(users.get_user(uuid=req.id))

    if user.synthetic:
        return InvalidProfile

    textures = handle_status(textures.get(uuid=req.id))

    texture_prop = TextureResponse(
        timestamp=int(datetime.now().timestamp() * 1000),
        profileId=user.uuid,
        profileName=user.login,
        textures=textures
    ).pack()

    raw_props = [texture_prop, *user.properties]

    if req.unsigned:
        properties = raw_props
    else:
        properties = [
            sign_property(private_key=config.key_pair.private, prop=prop)
            for prop
            in raw_props
        ]

    return JoinedResponse(
        id=user.uuid,
        name=user.login,
        properties=properties
    )


__all__ = {"join", "has_joined", "profile"}
