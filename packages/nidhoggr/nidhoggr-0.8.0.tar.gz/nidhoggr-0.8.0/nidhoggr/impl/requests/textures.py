from typing import Dict, Union

from nidhoggr_core.repository import BaseTextureRepo
from nidhoggr_core.response import ErrorResponse
from nidhoggr_core.texture import TextureType, TextureItem

from nidhoggr.impl.requests.core import RequestsRepo


class RequestsTextureRepo(BaseTextureRepo, RequestsRepo):

    def get(self, *, uuid: str) -> Union[ErrorResponse, Dict[TextureType, TextureItem]]:
        payload = {'uuid': uuid}
        result = self.fetch(endpoint='/texture/get', payload=payload)

        if isinstance(result, ErrorResponse):
            return result

        return {
            TextureType(kind): TextureItem(url=url)
            for kind, url
            in result.items()
        }
