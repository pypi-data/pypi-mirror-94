import operator
from functools import reduce
from typing import Union, Optional

from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from lavender.models import Player, Token
from lavender.views.api.decorator import json_response
from nidhoggr_core.repository import BaseUserRepo
from nidhoggr_core.response import StatusResponse
from nidhoggr_core.user import UserRequest, User, PasswordRequest

from lavender.decorators import typed, internal


def _user_request_fields(req: UserRequest) -> Optional[Q]:
    filters = []
    if req.login is not None:
        filters.append(Q(username=req.login))
    if req.email is not None:
        filters.append(Q(email=req.email))
    if req.uuid is not None:
        filters.append(Q(token__uuid=req.uuid))
    if req.access is not None:
        filters.append(Q(token__access=req.access))
    if req.client is not None:
        filters.append(Q(token__client=req.client))
    if req.server is not None:
        filters.append(Q(token__server_id=req.server))
    if not filters:
        return None
    return reduce(operator.or_, filters)


@csrf_exempt
@internal
@json_response
@typed
def get(req: UserRequest) -> Union[StatusResponse, User]:
    filters = _user_request_fields(req)
    if filters is None:
        return StatusResponse(status=False, reason="No valid user filters")
    try:
        player: Player = Player.objects.select_related('token').get(filters)
    except (Player.DoesNotExist, Player.MultipleObjectsReturned):
        return BaseUserRepo.EMPTY_USER

    return User(
        uuid=player.token.uuid.hex,
        login=player.username,
        email=player.email,
        access=player.token.access,
        client=player.token.client,
        server=player.token.server_id,
        properties=[],
    )


@csrf_exempt
@internal
@json_response
@typed
def check_password(req: PasswordRequest) -> StatusResponse:
    try:
        player: Player = Player.objects.get(token__uuid=req.uuid)
    except (Player.DoesNotExist, Player.MultipleObjectsReturned):
        return StatusResponse(status=False, reason=f"No such user with uuid {req.uuid}")
    status = player.check_password(req.password)
    return StatusResponse(status=status)


@csrf_exempt
@internal
@json_response
@typed
def save(req: User) -> StatusResponse:
    try:
        token: Token = Token.objects.get(uuid=req.uuid)
    except (Token.DoesNotExist, Token.MultipleObjectsReturned):
        return StatusResponse(status=False, reason=f"No such user with uuid {req.uuid}")

    # Do not alter any of user's properties (by now)
    token.access = req.access
    token.client = req.client
    token.server_id = req.server
    token.save()
    return StatusResponse(status=True)
