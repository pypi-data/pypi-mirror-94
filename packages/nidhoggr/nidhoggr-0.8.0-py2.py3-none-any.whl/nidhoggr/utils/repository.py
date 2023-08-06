from typing import Union, TypeVar

from nidhoggr_core.response import ErrorResponse
from werkzeug.exceptions import InternalServerError

T = TypeVar("T")


def handle_status(repository_response: Union[ErrorResponse, T]) -> T:
    if isinstance(repository_response, ErrorResponse):
        raise InternalServerError(description=repository_response.reason)
    return repository_response
