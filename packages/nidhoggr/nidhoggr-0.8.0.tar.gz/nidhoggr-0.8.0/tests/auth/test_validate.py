from nidhoggr.errors.auth import InvalidAccessToken, InvalidClientToken
from nidhoggr.errors.common import BadPayload
from ..conftest import cast


def test_empty_credentials(user, validate):
    assert cast[BadPayload](validate({}))
    assert cast[BadPayload](validate({"clientToken": user.client}))


def test_broken_access_token(user, validate):
    response = validate({
        "accessToken": "anything",
        "clientToken": user.client
    })
    assert response.status_code == 403
    assert cast[InvalidAccessToken](response)


def test_invalid_client_token(user, validate):
    response = validate({
        "accessToken": user.access,
        "clientToken": "anything"
    })
    assert response.status_code == 403
    assert cast[InvalidClientToken](response)


def test_validate_full(user, validate):
    response = validate({
        "accessToken": user.access,
        "clientToken": user.client
    })
    assert response.status_code == 204
    assert response.data == b""


def test_validate_simple(user, validate):
    response = validate({
        "accessToken": user.access,
    })
    assert response.status_code == 204
    assert response.data == b""
