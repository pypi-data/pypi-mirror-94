from functools import partial

import pytest
from flask.testing import FlaskClient

from nidhoggr.views import auth
from ..conftest import accessor, EndpointCallable


@pytest.fixture
def authenticate(client: FlaskClient) -> EndpointCallable:
    return partial(accessor(auth.authenticate), client)


@pytest.fixture
def refresh(client: FlaskClient) -> EndpointCallable:
    return partial(accessor(auth.refresh), client)


@pytest.fixture
def validate(client: FlaskClient) -> EndpointCallable:
    return partial(accessor(auth.validate), client)


@pytest.fixture
def invalidate(client: FlaskClient) -> EndpointCallable:
    return partial(accessor(auth.invalidate), client)


@pytest.fixture
def signout(client: FlaskClient) -> EndpointCallable:
    return partial(accessor(auth.signout), client)


def check_uuid(uuid: str):
    assert isinstance(uuid, str)
    assert len(uuid) == 32
    assert isinstance(int(uuid, 16), int)
