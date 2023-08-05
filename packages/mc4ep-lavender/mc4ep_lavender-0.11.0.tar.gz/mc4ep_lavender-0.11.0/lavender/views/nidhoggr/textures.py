from typing import Union

from django.views.decorators.csrf import csrf_exempt
from lavender.views.api.decorator import json_response
from nidhoggr_core.response import ErrorResponse
from nidhoggr_core.texture import TextureResponse, TextureRequest

from lavender.decorators import typed, internal


@csrf_exempt
@internal
@json_response
@typed
def get(req: TextureRequest) -> Union[ErrorResponse, TextureResponse]:
    # FIXME: Dummy implementation
    return TextureResponse(textures={})
