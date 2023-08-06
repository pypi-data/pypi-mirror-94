from nidhoggr_core.repository import BaseUserRepo
from nidhoggr.errors.auth import InvalidProfile
from nidhoggr.errors.common import BadPayload
from nidhoggr.utils.crypto import generate_uuid
from ..conftest import cast


def test_empty_credentials(user, join):
    assert cast[BadPayload](join({}))
    assert cast[BadPayload](join({"accessToken": user.access}))
    assert cast[BadPayload](join({"selectedProfile": user.uuid}))
    assert cast[BadPayload](join({"serverId": generate_uuid()}))
    assert cast[BadPayload](join({"accessToken": user.access, "selectedProfile": user.uuid}))
    assert cast[BadPayload](join({"accessToken": user.access, "serverId": generate_uuid()}))
    assert cast[BadPayload](join({"selectedProfile": user.access, "serverId": generate_uuid()}))


def test_invalid_profile(user, join):
    response = join({
        "accessToken": user.access,
        "selectedProfile": "anything",
        "serverId": generate_uuid()
    })
    assert cast[InvalidProfile](response)


def test_nonexistent_user(user, join):
    server_id = generate_uuid()
    response = join({
        "accessToken": "anything",
        "selectedProfile": user.uuid,
        "serverId": server_id
    })

    assert cast[InvalidProfile](response)


def test_join(users: BaseUserRepo, user, join):
    server_id = generate_uuid()
    response = join({
        "accessToken": user.access,
        "selectedProfile": user.uuid,
        "serverId": server_id
    })
    assert response.status_code == 204
    assert response.data == b""
    fresh = users.get_user(uuid=user.uuid)
    assert fresh.server == server_id
