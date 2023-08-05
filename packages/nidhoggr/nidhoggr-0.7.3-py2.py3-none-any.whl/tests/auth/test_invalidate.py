from nidhoggr_core.repository import BaseUserRepo
from nidhoggr.errors.auth import InvalidAccessToken, InvalidClientToken
from nidhoggr.errors.common import BadPayload
from ..conftest import cast


def test_empty_credentials(user, invalidate):
    assert cast[BadPayload](invalidate({}))
    assert cast[BadPayload](invalidate({"accessToken": user.access}))
    assert cast[BadPayload](invalidate({"clientToken": user.client}))
    assert cast[BadPayload](invalidate({"clientToken": user.client}))


def test_broken_access_token(user, invalidate):
    response = invalidate({
        "accessToken": "anything",
        "clientToken": user.client
    })
    assert response.status_code == 403
    assert cast[InvalidAccessToken](response)


def test_invalid_client_token(user, invalidate):
    response = invalidate({
        "accessToken": user.access,
        "clientToken": "anything"
    })
    assert response.status_code == 403
    assert cast[InvalidClientToken](response)


def test_invalidate_full(users: BaseUserRepo, user, invalidate):
    response = invalidate({
        "accessToken": user.access,
        "clientToken": user.client
    })
    assert response.status_code == 204
    assert response.data == b""
    fresh = users.get_user(uuid=user.uuid)
    assert fresh.access is None
